# mymodule.py
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from scipy import stats
from matplotlib import rcParams

# Set font properties for matplotlib (supports Chinese characters)
rcParams['font.family'] = 'Consolas'
rcParams['font.sans-serif'] = ['Microsoft Yahei']
class expo:
    def __init__(self):
        self.theta = np.array([])  # Input values θ
        self.alpha = np.array([])  # Output values α
        self.scaler_theta = StandardScaler()  # 用于标准化 θ 的 Scaler
        self.scaler_alpha = StandardScaler()  # 用于标准化 α 的 Scaler
        self.mintheta=100000000000
        self.maxtheta=-100000000000
        self.minalpha=100000000000
        self.maxalpha=-100000000000
    def train(self, data):
        """
        Add input data to the model.
        
        Args:
            data: Single tuple (θ, α) or list of tuples [(θ, α), (θ, α), ...]
        """
        if isinstance(data, tuple):
            self.mintheta=min(data[0],self.mintheta)
            self.maxtheta=max(data[0],self.maxtheta)
            self.minalpha=min(data[1],self.minalpha)
            self.maxalpha=max(data[1],self.maxalpha)            
            data = [data]  # Make data a list if it's a single tuple
            """
            if len(self.alpha)+1>5:
                raise RuntimeError("We are sorry that no more than 5 dots can be added. "\
                                   "This is because of the dimension limit of numpy. "\
                                   "We are trying to fix this bug as soon as possible. "\
                                   "If there is an available update, please check it as well.")
            """
        else:
            for i in data:
                self.mintheta=min(i[0],self.mintheta)
                self.maxtheta=max(i[0],self.maxtheta)
                self.minalpha=min(i[1],self.minalpha)
                self.maxalpha=max(i[1],self.maxalpha)
            """
            if len(self.alpha)+len(data)>5:
                raise RuntimeError("We are sorry that no more than 5 dots can be added. "\
                                   "This is because of the dimension limit of numpy. "\
                                   "We are trying to fix this bug as soon as possible. "\
                                   "If there is an available update, please check it as well.")
            """
        data = np.array(data)  # Convert to numpy array for easier manipulation
        self.theta = np.append(self.theta, data[:, 0])  # Add θ values
        self.alpha = np.append(self.alpha, data[:, 1])  # Add α values
        self.scaler_theta.fit(self.theta.reshape(-1, 1))  # Fit scaler to theta
        self.scaler_alpha.fit(self.alpha.reshape(-1, 1))  # Fit scaler to alpha
        self.theta_scaled = self.scaler_theta.transform(self.theta.reshape(-1, 1)).flatten()
        self.alpha_scaled = self.scaler_alpha.transform(self.alpha.reshape(-1, 1)).flatten()

    def calculate_rmse(self, true_values, predicted_values):
        """
        Calculate the Root Mean Squared Error (RMSE).
        """
        return np.sqrt(mean_squared_error(true_values, predicted_values))

    def calculate_aic(self, n, rss, p):
        """
        Calculate the Akaike Information Criterion (AIC).
        """
        return n * np.log(rss / n) + 2 * p

    def calculate_bic(self, n, rss, p):
        """
        Calculate the Bayesian Information Criterion (BIC).
        """
        return n * np.log(rss / n) + p * np.log(n)

    def detect_inflection_points(self, x, y):
        """
        Detect inflection points (change in concavity) in the data.
        """
        dy = np.gradient(y, x)  # First derivative
        ddy = np.gradient(dy, x)  # Second derivative
        inflection_points = np.where(np.diff(np.sign(ddy)))[0] + 1
        return inflection_points

    def fit_polynomial(self, max_degree=5):
        """
        Fit polynomial models to the data, choosing the best degree based on RMSE, AIC, and BIC.
        """
    def fit_polynomial(self, max_degree=5):
        """
        Fit polynomial models to the data, choosing the best degree based on RMSE, AIC, and BIC.
        """
        # 标准化数据
        theta_scaled = self.scaler_theta.transform(self.theta.reshape(-1, 1)).flatten()
        alpha_scaled = self.scaler_alpha.transform(self.alpha.reshape(-1, 1)).flatten()

        best_rmse = float('inf')
        best_aic = float('inf')
        best_bic = float('inf')
        best_degree = 1
        best_poly = None
        best_alpha_fit = None
        inflection_points = self.detect_inflection_points(theta_scaled, alpha_scaled)
        # Segment the data if there are inflection points
        if len(inflection_points) > 0:
            segments = np.split(np.column_stack((self.theta, self.alpha)), inflection_points)
        else:
            segments = [np.column_stack((self.theta, self.alpha))]

        all_fits = []

        for segment in segments:
            theta_segment = segment[:, 0]
            alpha_segment = segment[:, 1]

            if len(theta_segment) > 1:  # Check if data is sufficient for splitting
                X_train, X_test, y_train, y_test = train_test_split(theta_segment, alpha_segment, test_size=0.2, random_state=42)
                train_split = True
            else:
                X_train, X_test, y_train, y_test = theta_segment, theta_segment, alpha_segment, alpha_segment
                train_split = False

            # Fit polynomials for each segment
            for degree in range(1, max_degree + 1):
                try:
                    coeffs = np.polyfit(X_train, y_train, degree)
                    poly = np.poly1d(coeffs)
                    alpha_fit = poly(X_train)
                    theta_segment_scaled = self.scaler_theta.transform(theta_segment.reshape(-1, 1)).flatten()
                    alpha_segment_scaled = self.scaler_alpha.transform(alpha_segment.reshape(-1, 1)).flatten()
                    alpha_fit_scaled = poly(theta_segment_scaled)
                    alpha_fit_original = self.scaler_alpha.inverse_transform(alpha_fit_scaled.reshape(-1, 1)).flatten()
                    # Calculate RMSE
                    rmse = self.calculate_rmse(y_train, alpha_fit)

                    if train_split:
                        alpha_test_fit = poly(X_test)
                        rmse_test = self.calculate_rmse(y_test, alpha_test_fit)
                    else:
                        rmse_test = rmse

                    # Calculate AIC and BIC
                    rss = np.sum((y_train - alpha_fit) ** 2)  # Residual sum of squares
                    aic = self.calculate_aic(len(self.theta), rss, degree + 1)
                    bic = self.calculate_bic(len(self.theta), rss, degree + 1)

                    # Select the best model based on RMSE, AIC, and BIC
                    if rmse_test < best_rmse or (rmse_test == best_rmse and aic < best_aic and bic < best_bic):
                        best_rmse = rmse_test
                        best_aic = aic
                        best_bic = bic
                        best_degree = degree
                        best_poly = poly
                        best_alpha_fit = alpha_fit
                    all_fits.append((theta_segment, alpha_segment, best_poly))
                except np.linalg.LinAlgError as e:
                    print(f"Error in polyfit for degree {degree}: {e}")
                    continue

        return best_degree, best_poly, best_alpha_fit, best_rmse, all_fits

    def display(self):
        """
        Fit the best polynomial and display the plot.
        """
        if len(self.alpha) < 3:
            raise RuntimeError("At least 3 dots needed!")
        print("Generating graph, please wait...")
        print("Note: If 'polyfit' or similar warnings are generated, please ignore them.")
        best_degree, best_poly, best_alpha_fit, best_rmse, all_fits = self.fit_polynomial()

        # 恢复标准化后的数据
        theta_original = self.scaler_theta.inverse_transform(self.theta.reshape(-1, 1)).flatten()
        alpha_original = self.scaler_alpha.inverse_transform(self.alpha.reshape(-1, 1)).flatten()

        print(f"Best fitting polynomial degree: {best_degree}")
        print(f"RMSE: {best_rmse}")
        print(f"Fitted polynomial: {best_poly}")

        plt.scatter(theta_original, alpha_original, color='red', label='Data points')
        theta_fit_scaled = np.linspace(self.mintheta, self.maxtheta, 100)
        theta_fit_original = self.scaler_theta.inverse_transform(theta_fit_scaled.reshape(-1, 1)).flatten()
        alpha_fit_original = self.scaler_alpha.inverse_transform(best_poly(theta_fit_scaled).reshape(-1, 1)).flatten()

        # 绘制整体拟合曲线
        plt.plot(theta_fit_original, alpha_fit_original, label=f'{best_degree} degree polynomial fit', color='blue')

        # Plot each segment's fitted curve
        """
        for segment in all_fits:
            theta_segment, alpha_segment, segment_poly = segment
            theta_segment_scaled = self.scaler_theta.transform(theta_segment.reshape(-1, 1)).flatten()
            alpha_segment_fit_scaled = segment_poly(theta_segment_scaled)
            theta_segment_original = self.scaler_theta.inverse_transform(theta_segment_scaled.reshape(-1, 1)).flatten()
            alpha_segment_fit_original = self.scaler_alpha.inverse_transform(alpha_segment_fit_scaled.reshape(-1, 1)).flatten()
            plt.plot(theta_segment_original, alpha_segment_fit_original, linestyle='--', label='Segment fit')
        """
        plt.xlabel('θ (fi_in)')
        plt.ylabel('α (fi_ret)')
        print("Theta fit range:", min(theta_fit_scaled), max(theta_fit_scaled))
        print("Alpha fit range:", min(alpha_fit_original), max(alpha_fit_original))
        plt.title(f'Best fitting model: {best_degree} degree polynomial')
        plt.legend()
        plt.show()
if __name__=="__main__":
    print("This is a module, and cannot be directly run.")
    print("Please try \"from sestheta import *\".")
