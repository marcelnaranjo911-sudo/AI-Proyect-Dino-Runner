import numpy as np

class RedNeuronal:
    def __init__(self):
        self.input_size = 7
        self.hidden_size = 16 
        self.output_size = 2
        
        self.W1 = np.random.randn(self.input_size, self.hidden_size)
        self.W2 = np.random.randn(self.hidden_size, self.output_size)
        self.b1 = np.zeros((1, self.hidden_size))
        self.b2 = np.zeros((1, self.output_size))

    def relu(self, x):
        return np.maximum(0, x)

    def pensar(self, entradas):
        X = np.array(entradas).reshape(1, -1)
        Z1 = np.dot(X, self.W1) + self.b1
        A1 = self.relu(Z1)
        Z2 = np.dot(A1, self.W2) + self.b2
        return Z2[0] 

    def mutar(self, tasa_mutacion=0.1):
        self.W1 += np.random.randn(*self.W1.shape) * tasa_mutacion
        self.W2 += np.random.randn(*self.W2.shape) * tasa_mutacion
        self.b1 += np.random.randn(*self.b1.shape) * tasa_mutacion
        self.b2 += np.random.randn(*self.b2.shape) * tasa_mutacion

    def guardar(self, archivo):
        np.savez(archivo, W1=self.W1, W2=self.W2, b1=self.b1, b2=self.b2)

    def cargar(self, archivo):
        try:
            datos = np.load(archivo)
            self.W1 = datos['W1']
            self.W2 = datos['W2']
            self.b1 = datos['b1']
            self.b2 = datos['b2']
            return True
        except FileNotFoundError:
            return False