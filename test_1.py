import torch
import princess as pr
import supervise_log as log



class test_module(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.l = torch.nn.Linear(2,2)

    def forward(self, x):
        y = self.l(x)
        return y



def train():
    import time
    lr = 1e-4
    x = 10*torch.rand((1000,2))
    w = torch.tensor([[2.,3.],[1.,4.]])
    y = x.matmul(w) + 0.5 + torch.rand((1,))


    net = test_module()

    loss_f = torch.nn.MSELoss()
    op = torch.optim.Adam(net.parameters())

    logging = log.log(1)
    for i in range(2):
        for (j,(k,l)) in enumerate(zip(x,y)):
            y1 = net(k)
            loss = loss_f(y1,l)
            loss.backward()
            op.step()
            op.zero_grad()
            if j%500 == 0:
                #time.sleep(0.3)
                #print(loss.data.tolist())

                print(net.l.weight.data,net.l.bias.data)
                #print(net.l.weight,net.l.bias)
                logging.log_scalar(loss.data.tolist())
                logging.log_end()


if __name__ == "__main__":
    f = pr.Figure()
    f.add_scalar(0,'loss')
    f.write(train)



