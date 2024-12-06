import numpy as np

class SVM_Dual:
    def __init__(self, X, y, C=1, kernel='linear', b=0, max_iter=300, tol=1e-5, eps=1e-8):
        self.X = X
        self.y = y
        self.m, self.n = np.shape(self.X)
        self.C = C

        self.alphas = np.zeros(self.m)
        self.b = b

        self.kernel = kernel       # 'linear', 'rbf'
        if kernel == 'linear':
            self.kernel_func = self.linear_kernel
        elif kernel == 'gaussian' or kernel == 'rbf':
            self.kernel_func = self.gaussian_kernel
        else:
            raise ValueError('unknown kernel type')

        self.error = np.zeros(self.m)

        self.max_iter=max_iter
        self.tol = tol
        self.eps = eps

        self.is_linear_kernel = True if self.kernel == 'linear' else False
        self.w = np.zeros(self.n)  # used by linear kernel

    def linear_kernel(self, x1, x2, b=0):
        return x1 @ x2.T + b

    def gaussian_kernel(self, x1, x2, sigma=1):
        if np.ndim(x1) == 1 and np.ndim(x2) == 1:
            return np.exp(-(np.linalg.norm(x1-x2,2))**2/(2*sigma**2))
        elif(np.ndim(x1)>1 and np.ndim(x2) == 1) or (np.ndim(x1) == 1 and np.ndim(x2)>1):
            return np.exp(-(np.linalg.norm(x1-x2, 2, axis=1)**2)/(2*sigma**2))
        elif np.ndim(x1) > 1 and np.ndim(x2) > 1 :
            return np.exp(-(np.linalg.norm(x1[:, np.newaxis] \
                             - x2[np.newaxis, :], 2, axis = 2) ** 2)/(2*sigma**2))
        return 0.

    def predict(self, x):
        result = (self.alphas * self.y) @ self.kernel_func(self.X, x) + self.b
        return result

    def get_error(self, i):
        return self.predict(self.X[i,:]) - self.y[i]

    def take_step(self, i1, i2):
        if (i1 == i2):
            return 0

        x1 = self.X[i1, :]
        x2 = self.X[i2, :]

        y1 = self.y[i1]
        y2 = self.y[i2]

        alpha1 = self.alphas[i1]
        alpha2 = self.alphas[i2]

        b = self.b

        E1 = self.get_error(i1)
        E2 = self.get_error(i2)

        s = y1 * y2

        if y1 != y2:
            L = max(0, alpha2 - alpha1)
            H = min(self.C, self.C + alpha2 - alpha1)
        else:
            L = max(0, alpha2 + alpha1 - self.C)
            H = min(self.C, alpha2 + alpha1)

        if L == H:
            return 0

        k11 = self.kernel_func(x1, x1)
        k12 = self.kernel_func(x1, x2)
        k22 = self.kernel_func(x2, x2)

        eta = k11 + k22 - 2 * k12

        if eta > 0:
            alpha2_new = alpha2 + y2 * (E1 - E2) / eta
            if alpha2_new >= H:
                alpha2_new = H
            elif alpha2_new <= L:
                alpha2_new = L
        else:
            # Abnormal case for eta <= 0, treat this scenario as no progress
            return 0

        # Numerical tolerance
        # if abs(alpha2_new - alpha2) < self.eps:   # this is slower
        # below is faster, not degrade the SVM performance
        if abs(alpha2_new - alpha2) < self.eps * (alpha2 + alpha2_new + self.eps):
            return 0

        alpha1_new = alpha1 + s * (alpha2 - alpha2_new)

        # Numerical tolerance
        if alpha1_new < self.eps:
            alpha1_new = 0
        elif alpha1_new > (self.C - self.eps):
            alpha1_new = self.C

        # Update threshold
        b1 = b - E1 - y1 * (alpha1_new - alpha1) * k11 - y2 * (alpha2_new - alpha2) * k12
        b2 = b - E2 - y1 * (alpha1_new - alpha1) * k12 - y2 * (alpha2_new - alpha2) * k22
        if 0 < alpha1_new < self.C:
            self.b = b1
        elif 0 < alpha2_new < self.C:
            self.b = b2
        else:
            self.b = 0.5 * (b1 + b2)

        # Update weight vector for linear SVM
        if self.is_linear_kernel:
            self.w = self.w + y1 * (alpha1_new - alpha1) * x1 \
                            + y2 * (alpha2_new - alpha2) * x2

        self.alphas[i1] = alpha1_new
        self.alphas[i2] = alpha2_new

        # Error cache update
        ## if alpha1 & alpha2 are not at bounds, the error will be 0
        self.error[i1] = 0
        self.error[i2] = 0

        i_list = [idx for idx, alpha in enumerate(self.alphas) \
                      if 0 < alpha and alpha < self.C]
        for i in i_list:
            self.error[i] += \
                  y1 * (alpha1_new - alpha1) * self.kernel_func(x1, self.X[i,:]) \
                + y2 * (alpha2_new - alpha2) * self.kernel_func(x2, self.X[i,:]) \
                + (self.b - b)

        return 1


    def examine_example(self, i2):
        y2 = self.y[i2]
        alpha2 = self.alphas[i2]
        E2 = self.get_error(i2)
        r2 = E2 * y2

        # Choose the one that is likely to violiate KKT
        # if (0 < alpha2 < self.C) or (abs(r2) > self.tol):  # this is slow
        # below is faster, not degrade the SVM performance
        if ((r2 < -self.tol and alpha2 < self.C) or (r2 > self.tol and alpha2 > 0)):
            if len(self.alphas[(0 < self.alphas) & (self.alphas < self.C)]) > 1:
                if E2 > 0:
                    i1 = np.argmin(self.error)
                else:
                    i1 = np.argmax(self.error)

                if self.take_step(i1, i2):
                    return 1

            # loop over all non-zero and non-C alpha, starting at a random point
            i1_list = [idx for idx, alpha in enumerate(self.alphas) \
                           if 0 < alpha and alpha < self.C]
            i1_list = np.roll(i1_list, np.random.choice(np.arange(self.m)))
            for i1 in i1_list:
                if self.take_step(i1, i2):
                    return 1

            # loop over all possible i1, starting at a random point
            i1_list = np.roll(np.arange(self.m), np.random.choice(np.arange(self.m)))
            for i1 in i1_list:
                if self.take_step(i1, i2):
                    return 1

        return 0

    def fit(self):
        loop_num = 0
        numChanged = 0
        examineAll = True
        while numChanged > 0 or examineAll:
            if loop_num >= self.max_iter:
                break

            numChanged = 0
            if examineAll:
                for i2 in range(self.m):
                    numChanged += self.examine_example(i2)
            else:
                i2_list = [idx for idx, alpha in enumerate(self.alphas) \
                                if 0 < alpha and alpha < self.C]
                for i2 in i2_list:
                    numChanged += self.examine_example(i2)

            if examineAll:
                examineAll = False
            elif numChanged == 0:
                examineAll = True

            loop_num += 1




# def gen_circle(n=50, center_x=0, center_y=0, radius=1, label=0):

#     """
#     A simple function that generates circular distribution
#     n: number of points (default=50)
#     center_x: the center for X (default=0)
#     center_y: the center for Y (default=0)
#     radius: the radius of circle (default=1)
#     """

#     # random angle
#     alpha = 2 * np.pi * np.random.rand(n)
#     # random radius
#     r = radius * np.sqrt(np.random.rand(n))
#     # calculating coordinates
#     x = r * np.cos(alpha) + center_x
#     y = r * np.sin(alpha) + center_y

#     label = np.ones(n) * label

#     return [x, y, label]


# if __name__ == '__main__':
#     np.random.seed(5)   # to reproduce

#     n = 100
#     C0 = gen_circle(n, center_x=1, center_y=1, radius=1.05, label=1)
#     C1 = gen_circle(n, center_x=-1, center_y=-1, radius=1.05, label=-1)

#     x0 = np.append(C0[0], C1[0])
#     x1 = np.append(C0[1], C1[1])

#     X = np.c_[x0, x1]
#     Y = np.append(C0[2], C1[2])

#     scaler = StandardScaler()
#     train_x = scaler.fit_transform(X)

#     # model = SVM(train_x, Y, C=1, kernel='linear', max_iter=600, tol=1e-5, eps=1e-5)
#     model = SVM_Dual(train_x, Y, C=1, kernel='rbf', max_iter=600, tol=1e-5, eps=1e-5)
#     model.fit()

#     train_y = model.predict(train_x)

#     print('support vector: {} / {}'\
#         .format(len(model.alphas[model.alphas != 0]), len(model.alphas)))
#     sv_idx = []
#     for idx, alpha in enumerate(model.alphas):
#         if alpha != 0:
#             print('index = {}, alpha = {:.3f}, predict y={:.3f}'\
#                 .format(idx, alpha, train_y[idx]))
#             sv_idx.append(idx)


#     print(f'bias = {model.b}')
#     print('training data error rate = {}'.format(len(Y[Y * train_y < 0])/len(Y)))

#     ## Draw the Plot
#     plt.plot(C0[0], C0[1], 'o', markerfacecolor='r', markeredgecolor='None', alpha=0.55)
#     plt.plot(C1[0], C1[1], 'o', markerfacecolor='b', markeredgecolor='None', alpha=0.55)

#     resolution = 50
#     dx = np.linspace(X[:, 0].min(), X[:, 0].max(), resolution)
#     dy = np.linspace(X[:, 1].min(), X[:, 1].max(), resolution)
#     dx, dy = np.meshgrid(dx, dy)
#     plot_x = np.c_[dx.flatten(), dy.flatten()]

#     dz = model.predict(scaler.transform(plot_x))
#     dz = dz.reshape(dx.shape)

#     plt.contour(dx, dy, dz, alpha=1, colors=('b', 'k', 'r'), \
#                 levels=(-1, 0, 1), linestyles = ('--', '-', '--'))

#     label_cnt = 0
#     for i in sv_idx:
#         if label_cnt == 0:
#             plt.scatter(X[i, 0], X[i, 1], marker='*', color='k', \
#                         s=120, label='Support vector')
#             label_cnt += 1
#             continue

#         plt.scatter(X[i, 0], X[i, 1], marker='*', color='k', s=120)

#     plt.legend()
#     plt.show()