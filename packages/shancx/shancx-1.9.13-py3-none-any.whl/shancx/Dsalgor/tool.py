import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as transforms
from torchvision import transforms
import os
from PIL import Image
import numpy as np
from tqdm import tqdm
import glob

# 简化的 ResUNet 架构
class ResUNet(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(ResUNet, self).__init__()
        self.encoder = ResNetEncoder(in_channels)
        self.decoder = UNetDecoder(out_channels)
    
    def forward(self, x):
        enc_out = self.encoder(x)
        dec_out = self.decoder(enc_out)
        return dec_out

class ResNetEncoder(nn.Module):
    def __init__(self, in_channels):
        super(ResNetEncoder, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        # 可以继续添加更多层
        
    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        return x

class UNetDecoder(nn.Module):
    def __init__(self, out_channels):
        super(UNetDecoder, self).__init__()
        self.upconv = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
        self.final_conv = nn.Conv2d(128, out_channels, kernel_size=1)
    
    def forward(self, x):
        x = self.upconv(x)
        x = self.final_conv(x)
        return x

# 自定义数据集类
class SatelliteDataset(Dataset):
    def __init__(self, image_dir, mask_dir, transform=None):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.image_filenames = os.listdir(image_dir)
        self.mask_filenames = os.listdir(mask_dir)
        self.transform = transform

    def __len__(self):
        return len(self.image_filenames)

    def __getitem__(self, idx):
        img_name = self.image_filenames[idx]
        mask_name = self.mask_filenames[idx]
        
        img = Image.open(os.path.join(self.image_dir, img_name)).convert("RGB")
        mask = Image.open(os.path.join(self.mask_dir, mask_name)).convert("L")  # 单通道灰度图
        
        if self.transform:
            img = self.transform(img)
            mask = self.transform(mask)
        
        return img, mask

# 数据增强与预处理
transform = transforms.Compose([
    transforms.Resize((256, 256)),  # 调整图像大小
    transforms.ToTensor(),  # 转换为Tensor并归一化到[0, 1]
])
# 加载数据集
image_dir = 'path/to/your/images'  # 输入图像路径
mask_dir = 'path/to/your/masks'    # 分割掩膜路径
dataset = SatelliteDataset(image_dir, mask_dir, transform)
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)
# 定义模型、损失函数和优化器
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = ResUNet(in_channels=3, out_channels=1).to(device)  # 3个输入通道(RGB)，1个输出通道（二值化分割）
criterion = nn.BCEWithLogitsLoss()  # 用于二分类任务的损失函数
optimizer = optim.Adam(model.parameters(), lr=1e-4)
# 训练循环
num_epochs = 20
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0

    for imgs, masks in dataloader:
        imgs, masks = imgs.to(device), masks.to(device)

        # 正向传播
        outputs = model(imgs)
        
        # 计算损失
        loss = criterion(outputs.squeeze(1), masks.float())  # 去除多余的维度并将掩膜转换为float
        running_loss += loss.item()

        # 反向传播和优化
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    avg_loss = running_loss / len(dataloader)
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}")

# 保存训练好的模型
torch.save(model.state_dict(), 'resunet_model.pth')


"""
class ToTensorTarget(object):
    def __call__(self, sample):
        sat_img, map_img = sample["sat_img"], sample["map_img"]

        # swap color axis because
        # numpy image: H x W x C
        # torch image: C X H X W

        return {
            "sat_img": transforms.functional.to_tensor(sat_img).permute(1,2,0),  #(H, W, C) -->transforms.functional.to_tensor(sat_img)-->(C, H, W) --.permute(1,2,0)-->(H, W, C)  H 是图像的高度,W 是宽度,C 是通道数
            "map_img": torch.from_numpy(map_img).unsqueeze(0).float(),
        }  # unsqueeze for the channel dimension
        
# 自定义数据集类
class npyDataset_regression(Dataset):
    def __init__(self, args, train=True, transform=None):
        self.train = train
        self.path = args.train if train else args.valid
        self.mask_list = glob.glob(
            os.path.join(self.path, "mask", "*.npy"), recursive=True
        )
        self.transform = transform
    def __len__(self):
        return len(self.mask_list)
    def __getitem__(self, idx):
        try:    
               maskpath = self.mask_list[idx]
               image = np.load(maskpath.replace("mask", "input")).astype(np.float32)
               image = image[-2:,:,:]
               image[image<15] = np.nan
               ### 5-15dbz
               #image[image>20] = np.nan
               #image[image<5] = np.nan
               #mean = np.float32(9.81645766)
               #std = np.float32(10.172995)
               image_mask = image[-1,:,:].copy().reshape(256,256)
               image_mask[~np.isnan(image_mask)]=1
               #tmp = image[-2,:,:].reshape((256,256)) * image_mask
               #image[-2,:,:] = tmp.reshape((1,256,256))
               mask = np.load(maskpath).astype(np.float32)  
               mask = mask * image_mask
               image[np.isnan(image)]=0
               sample = {"x_img": image, "map_img": mask}
               if self.transform:
                   sample = self.transform(sample)
                   sample['maskpath'] = maskpath
               return sample
        except Exception as e:
               print(f"Error loading data at index {index}: {str(e)}")
               # 可以选择跳过当前样本或者返回一个默认值
               print(traceback.format_exc())
               loggers.info(traceback.format_exc())
               return None

dataset = npyDataset_regression(args, transform=transforms.Compose([ToTensorTarget()]))  #=transforms.Compose([dataloader_radar10.ToTensorTarget()])
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)
loader = tqdm(dataloader, desc="training")
for idx, data in enumerate(loader):
    inputs = data["x_img"].cuda()
    labels = data["map_img"].cuda()
    optimizer.zero_grad()
    outputs = model(inputs)
""" 