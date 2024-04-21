VideoProcess = list(range(60))
Div = len(VideoProcess) // 100
NewList = []
for Step in range(Div+1):
	NewList.append(VideoProcess[int(Step * (len(VideoProcess) / (Div + 1))) : int((Step + 1) * (len(VideoProcess) / (Div + 1)))])
print(NewList)