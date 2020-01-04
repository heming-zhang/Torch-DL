import os
from mnist_parse import ParseFile
from mnist_nn import RunMnistNN
from mnist_nn import MnistNNPlot
from mnist_nn import MnistNNLoad
from mnist_nn import MnistParameter

def parse_file():
    train_img = "./MNIST/train-images-idx3-ubyte"
    train_label = "./MNIST/train-labels-idx1-ubyte"
    test_img = "./MNIST/t10k-images-idx3-ubyte"
    test_label = "./MNIST/t10k-labels-idx1-ubyte"
    ParseFile(train_img, train_label, 0).parse_image()
    ParseFile(train_img, train_label, 0).parse_label()
    ParseFile(test_img, test_label, 0).parse_image()
    ParseFile(test_img, test_label, 0).parse_label()

def classify_file():
    train_img = "./MNIST/train-images-idx3-ubyte"
    train_label = "./MNIST/train-labels-idx1-ubyte"
    test_img = "./MNIST/t10k-images-idx3-ubyte"
    test_label = "./MNIST/t10k-labels-idx1-ubyte"
    for i in range(0, 10):
        ParseFile(train_img, train_label, i).classify()
        ParseFile(test_img, test_label, i).classify()

def run_mnist_nn(nn_batchsize, nn_worker,
            nn_learning_rate, nn_momentum, 
            nn_cuda, nn_epoch_num):
    # Load data with mini-batch
    train_loader, test_loader = MnistNNLoad(nn_batchsize, 
                nn_worker).load_data()
    # Use Neural Network as training model
    model, criterion, optimizer = MnistParameter(
                nn_learning_rate,
                nn_momentum,
                nn_cuda).mnist_function()
    # Get experimental results in every epoch
    train_accuracy_rate = []
    test_accuracy_rate = []
    for epoch in range(1, nn_epoch_num + 1):
        train_loss, train_accuracy = RunMnistNN(model,
                    criterion,
                    optimizer,
                    train_loader,
                    test_loader).train_mnist_nn()
        test_loss, test_accuracy = RunMnistNN(model,
                    criterion,
                    optimizer,
                    train_loader,
                    test_loader).test_mnist_nn()
        train_accuracy_rate.append(train_accuracy)
        test_accuracy_rate.append(test_accuracy)
        print(epoch, train_accuracy, test_accuracy)
    # Make plot for Mnist-NN model
    MnistNNPlot(train_accuracy_rate,
                test_accuracy_rate,
                nn_epoch_num).plot()

if __name__ == "__main__":
    if os.path.isdir("./mnist") == False:
        parse_file()
    if os.path.isdir("./mnist_classified") == False:
        classify_file()
    # Run Mnist Neural Network
    nn_batchsize = 640
    nn_worker = 2
    nn_learning_rate = 0.01
    nn_momentum = 0.5
    nn_cuda = False
    nn_epoch_num = 20
    run_mnist_nn(nn_batchsize, nn_worker, nn_learning_rate,
                nn_momentum, nn_cuda, nn_epoch_num)