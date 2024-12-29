import os
from PIL import Image

import torch
import torch.nn as nn
from torchvision import transforms


class CNN(nn.Module):
	def __init__(self, num_class=36, num_char=4):
			super(CNN, self).__init__()
			self.num_class = num_class
			self.num_char = num_char
			self.conv = nn.Sequential(

	            nn.Conv2d(3, 64, 3, padding=(1, 1)),
	            nn.MaxPool2d(2, 2),
	            nn.BatchNorm2d(64),
	            nn.ReLU(),

	            nn.Conv2d(64, 64, 3, padding=(1, 1)),
	            nn.MaxPool2d(2, 2),
	            nn.BatchNorm2d(64),
	            nn.ReLU(),

	            nn.Conv2d(64, 512, 3, padding=(1, 1)),
	            nn.BatchNorm2d(512),
	            nn.ReLU(),

				nn.Conv2d(512, 512, 3, padding=(1, 1)),
	            nn.BatchNorm2d(512),
	            nn.ReLU(),

				nn.Conv2d(512, 512, 3, padding=(1, 1)),
				nn.MaxPool2d(2, 2),
	            nn.BatchNorm2d(512),
	            nn.ReLU(),

	            nn.Conv2d(512, 512, 3, padding=(1, 1)),
	            nn.MaxPool2d(2, 2),
	            nn.BatchNorm2d(512),
	            nn.ReLU(),

	            )
			self.fc = nn.Linear(512*2*6, self.num_class*self.num_char)

	def forward(self, x):
		x = self.conv(x)
		
		x = x.view(-1, 512*2*6)
		x = self.fc(x)
		return x
	

model_path = os.path.join(os.getcwd(), r'CNN_predict\demo11.pth') # 模型路径


# 输入图片路径进行处理
def CNN_predict(img_path): 
	# 从路径读取图片
	try:
		img = Image.open(img_path).convert('RGB')  # 确保图像是RGB模式
	except FileNotFoundError:
		print(f'No such file: {img_path}')
		return

    # 判断并处理图片尺寸
	if img.size != (100, 45):
		print('image size not is (100, 45), it wiil be processed to one')
		img = img.resize((100, 45))  # 调整图片到期望的尺寸
	
    # 指定GPU或CPU
	device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # 将图片数据处理为张量
	transform = transforms.Compose([transforms.ToTensor()])
	input_tensor = transform(img).view(1, 3, 45, 100).to(device) # 输入张量移动到device
	
    # 加载模型
	model = CNN()
	state_dict = torch.load(model_path)
	model.load_state_dict(state_dict)
	model.to(device)
	
    # 改为评估模型
	model.eval()
	with torch.no_grad():
		output = model(input_tensor) 
	output = output.cpu() # 移动打CPU用于之后处理
	
    # SoftMax得到输出
	charset = 'abcdefghijklmnopqrstuvwxyz0123456789'
	output = output.view(1, 4, 36)
	output = nn.functional.softmax(output, dim=2)
	output = torch.argmax(output, dim=2)
	# 拼接字符串得到输出
	result = ''
	for i in output.flatten():
		result += charset[i]

	return result