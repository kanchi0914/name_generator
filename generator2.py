from scraper import Scraper
import torch
import torch.nn as nn
import torch.autograd as autograd
from torch.autograd import Variable
import torch.optim as optim
import random

scraper = Scraper()
datas = scraper.load_csv("csv/en_jp_names.csv")
names = [data[1] + "." for data in datas]


all_char_str = set([char for name in names for char in name])
char2idx = {char: i for i, char in enumerate(all_char_str)}
char2idx['EOS'] = len(char2idx)
print(len(char2idx))  # 66

names_idx = {v: k for k, v in char2idx.items()}

class LSTM(nn.Module):
    def __init__(self, input_dim, embed_dim, hidden_dim):
        super(LSTM, self).__init__()
        self.hidden_dim = hidden_dim
        self.embeds = nn.Embedding(input_dim, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim)
        self.linear = nn.Linear(hidden_dim, input_dim)
        self.dropout = nn.Dropout(0.1)
        self.softmax = nn.LogSoftmax(dim=1)
        self.hidden = self.initHidden()

    def forward(self, input, hidden):
        embeds = self.embeds(input)
        lstm_out, hidden = self.lstm(
            embeds.view(len(input), 1, -1), hidden)
        output = self.linear(lstm_out.view(len(input), -1))
        output = self.dropout(output)
        output = self.softmax(output)
        return output, hidden

    def initHidden(self):
        return (autograd.Variable(torch.zeros(1, 1, self.hidden_dim)),
                autograd.Variable(torch.zeros(1, 1, self.hidden_dim)))


def train(model, input, target):
    hidden = model.initHidden()

    model.zero_grad()

    output, _ = model(input, hidden)
    topv, topi = output.data.topk(1)
    _, predY = torch.max(output.data, 1)
    criterion = torch.nn.NLLLoss()
    loss = criterion(output, target)

    loss.backward()

    return loss.data[0] / input.size()[0]

def inputTensor(input_idx):
    tensor = torch.LongTensor(input_idx)
    return autograd.Variable(tensor)


def targetTensor(input_idx):
    input_idx = input_idx[1:]
    input_idx.append(char2idx['EOS'])
    tensor = torch.LongTensor(input_idx)
    return autograd.Variable(tensor)


# build model
model = LSTM(input_dim=len(char2idx), embed_dim=100, hidden_dim=128)

criterion = nn.NLLLoss()
optimizer = optim.RMSprop(model.parameters(), lr=0.001)

n_iters = 4
all_losses = []

for iter in range(1, n_iters + 1):

    # data shuffle
    random.shuffle(names_idx)

    total_loss = 0

    for i, name_idx in enumerate(names_idx):
        input = inputTensor(name_idx)
        target = targetTensor([name_idx])

        loss = train(model, input, target)
        total_loss += loss

        optimizer.step()

    print(iter, "/", n_iters)
    print("loss {:.4}".format(float(total_loss / len(names_idx))))