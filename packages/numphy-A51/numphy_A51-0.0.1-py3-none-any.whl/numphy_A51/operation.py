def mdalabs():
    lab = input()

    if lab == 'mdalab1':
        code =   """
                    ## Basic data preprocessing and plotting fitting linear regression mean, covaraince and correlation matrix

                    import numpy as np
                    import pandas as pd
                    import matplotlib as mpl
                    import matplotlib.pyplot as plt
                    from sklearn.linear_model import LinearRegression
                    from sklearn.preprocessing import PolynomialFeatures

                    data = pd.read_excel("/content/drive/MyDrive/Colab Notebooks/MDA/DATA/DATA/HeightWeight.xlsx")
                    data.head()

                    # 1. Scatter Plot
                    plt.scatter(data['Height'], data['Weight'])
                    plt.xlabel('Height (inches)')
                    plt.ylabel('Weight (lbs)')
                    plt.title('Height vs Weight Scatter Plot')
                    plt.show()

                    X = data['Height'].values.reshape(-1, 1)
                    y = data['Weight'].values
                    model = LinearRegression().fit(X, y)
                    plt.scatter(X, y)
                    plt.plot(X, model.predict(X), color='red')
                    plt.xlabel('Height (inches)')
                    plt.ylabel('Weight (lbs)')
                    plt.title('Linear Regression of Height vs Weight')
                    plt.show()

                    # 2. polynomial regression model
                    # Prepare the data
                    X = data['Height'].values.reshape(-1, 1)
                    y = data['Weight'].values
                    # Fit a polynomial regression model
                    poly_features = PolynomialFeatures(degree=2) # You can adjust the degree for higher order polynomials
                    X_poly = poly_features.fit_transform(X)
                    model = LinearRegression().fit(X_poly, y)
                    # Visualize the polynomial regression model
                    plt.scatter(X, y)
                    plt.plot(X, model.predict(X_poly), color='red')
                    plt.xlabel('Height (inches)')
                    plt.ylabel('Weight (lbs)')
                    plt.title('Polynomial Regression of Height vs Weight')
                    plt.show()

                    # 3. Mean, Covariance, Correlation
                    mean_vector = np.mean(data, axis=0)
                    covariance_matrix = np.cov(data.T)
                    correlation_matrix = np.corrcoef(data.T)
                    print("Mean Vector:\n", mean_vector)
                    print("\nCovariance Matrix:\n", covariance_matrix)
                    print("\nCorrelation Matrix:\n", correlation_matrix)

                    # 4. Conversion to Meters and Kilograms (Matrix Operation)
                    conversion_matrix = np.array([[0.0254, 0], # inches to meters
                    [0, 0.453592]]) # lbs to kg
                    new_data = data.values @ conversion_matrix
                    new_df = pd.DataFrame(new_data, columns=['Height (m)', 'Weight (kg)'])
                    print("\nDataset in meters and kilograms:\n", new_df)

                    scores = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/MDA/DATA/DATA/3judges.csv")
                    scores.head()

                    import pandas as pd
                    # Assuming 'scores' DataFrame is already loaded as in the preceding code
                    # Calculate the average score for each judge
                    average_scores = scores.mean()
                    # Find the judge with the highest average score
                    highest_scoring_judge = average_scores.idxmax()

                    print(f'The judge who gives the highest scores on average is:␣{highest_scoring_judge}')

                    import numpy as np
                    # 2. Total and Average Scores
                    total_scores = scores.sum(axis=1) # Sum along rows (each contestant)
                    average_scores = scores.mean(axis=1)
                    print("Total Scores per Contestant:", total_scores)
                    print("Average Scores per Contestant:", average_scores)
                    # 3. New Weighted Scoring Scheme
                    weights1 = np.array([0.5, 1.25, 1.25])
                    weighted_scores1 = scores * weights1 # Element-wise multiplication
                    total_weighted_scores1 = weighted_scores1.sum(axis=1)
                    print("\nTotal Weighted Scores (Scheme 1):", total_weighted_scores1)
                    # 4. Judge 1's Proposed Scheme (Average)
                    weights2 = np.array([0.5, 1.0, 1.0])
                    weighted_scores2 = scores * weights2
                    average_weighted_scores2 = weighted_scores2.mean(axis=1)
                    print("\nAverage Weighted Scores (Scheme 2):", average_weighted_scores2)"""
        return code
    
    if lab == 'mdalab2':
        code =   """
                    ## Confidence Ellipse-1

                    import pandas as pd
                    import numpy as np
                    import matplotlib.pyplot as plt
                    import scipy.linalg as la
                    from scipy.stats import norm,chi2

                    # Genterate two or more n random noraml observationn X with mean zero and
                    # std 1, Perform cholesky decompostion of the given co-variance matrix( sigma
                    # and take the lower triangular matrix L from that (L * transpose(L) = Sigma),
                    # pre multiply the L with X, Now this will have the mean Mu and the

                    def generate_correlated_data(num_samples,mu,cov_mat):
                        init_x=norm.rvs(size=(len(cov_mat),num_samples),random_state=101)
                        C = la.cholesky(cov_mat,lower=True)
                        X = np.dot(C,init_x)
                        # move the center ti mu
                        X=X+np.outer(np.ones(num_samples),mu).transpose()
                        return X

                    cov_mat = np.array([[1.1, -1], [-1, 1]])
                    mu = np.array([0, 0])
                    X= np.random.multivariate_normal(mean=[0,0],cov= cov_mat,size=100).transpose()
                    np.corrcoef(X[0],X[1])

                    rhos = np.array([-1, -0.75, -0.5,-0.25,0,0.25,0.5,0.75,1])
                    rhos_mesh = rhos.reshape(3,3)
                    rhos_mesh

                    # Plotting the simultaed data for the different correlation values

                    num_samples=1000
                    mu=[0,0]
                    rhos = np.array([-1, -0.75, -0.5,-0.25,0,0.25,0.5,0.75,1])
                    rhos_mesh = rhos.reshape(3,3)
                    nrows,ncols = rhos_mesh.shape
                    fig,axes = plt.subplots(figsize=(10,10),nrows=nrows,ncols=ncols)
                    for rhos_row,row_axes in zip(rhos_mesh,axes):
                        for rho,ax in zip(rhos_row,row_axes):
                            cov_mat = [[1.1,rho],[rho,1]]
                            X = generate_correlated_data(num_samples,mu,cov_mat)
                            ax.scatter(X[0],X[1])
                            ax.scatter(mu[0],mu[1],s=30,c="red")
                            ax.axhline(mu[1],c="red",lw=0.5)
                            ax.axvline(mu[0],c="red",lw=0.5)
                            corr_computed = np.corrcoef(X[0],X[1])[0,1].round(2)
                            ax.set_title(f'corr={corr_computed}')
                    plt.show()

                    # Plotting for individual

                    init_x = norm.rvs(size=(2, 1000))
                    cov_mat = np.array([[1.1, -1], [-1, 1]])
                    mu = np.array([0,0])
                    X= generate_correlated_data(num_samples=1000,mu=mu,cov_mat = cov_mat)
                    corr_= np.corrcoef(X[0],X[1])[0,1].round(2)
                    plt.scatter(X[0],X[1])
                    plt.title(f'corr={corr_}')
                    plt.show()

                    # Generating Univariate Normal Data and Displaying Q-Q Plot

                    num_samples=1000
                    mu=[1,2]

                    #Write a code that generate univariate normal data and show QQ plot
                    import numpy as np
                    import matplotlib.pyplot as plt
                    import statsmodels.api as sm

                    # Generate random normally distributed data
                    data = np.random.normal(0, 1, 1000)
                    # Create QQ plot
                    sm.qqplot(data, line='45')
                    plt.title('Q-Q Plot')
                    plt.show()

                    # Q-Q Plot Generation without Direct Sort Command
                    import numpy as np
                    import matplotlib.pyplot as plt
                    import statsmodels.api as sm

                    # Generate random normally distributed data
                    data = np.random.normal(0, 1, 1000)
                    # Sort the data in ascending order
                    sorted_data = np.sort(data)
                    # Calculate the theoretical quantiles
                    n = len(sorted_data)
                    quantiles = np.arange(1, n + 1) / (n + 1)
                    # Calculate the quantiles based on a normal distribution
                    norm_quantiles = np.quantile(np.random.normal(0, 1, 1000), quantiles)

                    # Create QQ plot using the sorted data and calculated quantiles
                    plt.figure(figsize=(6, 6))
                    plt.scatter(norm_quantiles, sorted_data)
                    plt.plot([-3, 3], [-3, 3], color='red', linestyle='--') # 45-degree line
                    plt.title('Q-Q Plot')
                    plt.xlabel('Theoretical Quantiles')
                    plt.ylabel('Ordered Values')
                    plt.show()"""
        return code
    
    if lab == 'mdalab3':
        code =   """
                    ## Confidence Ellispe-2
        
                    from matplotlib.patches import Ellipse
                    import pandas as pd
                    import numpy as np
                    import matplotlib.pyplot as plt
                    import scipy.linalg as la
                    from scipy.stats import norm,chi2

                    def generate_correlated_data(num_samples,mu,cov_mat):
                        init_x=norm.rvs(size=(len(cov_mat),num_samples),random_state=101)
                        C = la.cholesky(cov_mat,lower=True)
                        X = np.dot(C,init_x)
                        # move the center ti mu
                        X=X+np.outer(np.ones(num_samples),mu).transpose()
                        return X

                    num_samples = 1000
                    mu = [1,2]
                    cov_mat= [[1.1,0.75],[0.75,1]]
                    X = generate_correlated_data(num_samples,mu,cov_mat)
                    data= pd.DataFrame(X.transpose())
                    data.head()

                    def draw_confidence_ellipse(data,alpha ,**kwargs):
                        dof = len(data.columns)
                        p = dof
                        n = len(data)
                        if n-p > 40:
                        c= np.sqrt(chi2.ppf(1-alpha,dof))

                        mean_vec = np.array(data.mean())
                        cov_matrix= np.array(data.cov())
                        # find the eigenvalues and eigenvectors
                        eigvals,eigvecs = la.eigh(cov_matrix)
                        #Sorting based on descnding oirder of eigen values
                        order=eigvals.argsort()[::-1]
                        eigvals = eigvals[order]
                        eigvecs = eigvecs[:,order]
                        #Width and height of the ellipse to draw
                        width, height = 2* c * np.sqrt(eigvals)
                        #Angles of the major axis
                        vx,vy = eigvecs[:,0][0],eigvecs[:,0][1]
                        angle = np.degrees(np.arctan2(vy,vx))
                        return Ellipse(xy = mean_vec,   
                        width = width,
                        height = height,
                        angle = angle,
                        fill = False,
                        label = f"{100*(1-alpha):.0f}%",**kwargs)

                    def plot_data_confidence_ellipse(data,ax,alphas = [0.01,0.05,0.1],colors = ["red","blue","yellow"]):
                        ax.scatter(data[0],data[1])
                        ax.scatter(data.mean()[0],data.mean()[1],s=100)
                        for alpha,color in zip(alphas,colors):
                            e = draw_confidence_ellipse(data,alpha = alpha,color = color,lw=2)
                            ax.add_patch(e)

                    def plot_confidence_regions(data,ax):
                        fig,ax = plt.subplots(figsize=(8,8))
                        plot_data_confidence_ellipse(data=data,ax=ax)
                        plt.legend()
                        plt.show()

                    plot_confidence_regions(data,ax)

                    num_samples=1000
                    mu=[0,0]
                    rhos = np.array([-1, -0.75, -0.5,-0.25,0,0.25,0.5,0.75,1])
                    rhos_mesh = rhos.reshape(3,3)
                    nrows,ncols = rhos_mesh.shape
                    fig,axes = plt.subplots(figsize=(10,10),nrows=nrows,ncols=ncols)
                    for rhos_row,row_axes in zip(rhos_mesh,axes):
                        for rho,ax in zip(rhos_row,row_axes):
                            cov_mat = [[1.1,rho],[rho,1]]
                            X = generate_correlated_data(num_samples,mu,cov_mat)
                            data = pd.DataFrame(X.transpose())
                            plot_data_confidence_ellipse(data=data,ax=ax)
                            ax.legend()
                            ax.set_title(f'correlation={data.corr()[0][1].round(2)}')
                    plt.show()"""
        
        return code
    if lab == 'mdalab4':
        code =   """ 
                    ## Correlation 
        
                    import matplotlib.pyplot as plt
                    import numpy as np
                    import pandas as pd
                    from scipy.stats import pearsonr

                    # Data
                    data = {
                    'National Park': ['Arcadia', 'Bruce Canyon', 'Cuyahoga Valley','Everglades', 'Grand Canyon', 'Grand Thton', 'Great Smoky', 'Hot Springs', 'Olympic', 'Mount Rainier','Rocky Mountain', 'Shenandoah','Yellowstone', 'Yosemite', 'Zion'],
                    'Size (acres)': [47.4, 35.8, 32.9, 1508.5, 1217.4, 310, 521.8, 5.6, 922.7, 235.6, 265.8, 199, 2219.8, 761.3, 146.6],
                    'Visitors (millions)': [2.05, 1.02, 2.53, 1.23, 4.4, 2.46, 9.19, 1.34, 3.14, 1.17, 2.8, 1.09, 2.84, 3.3, 2.59]
                    }
                    # Create DataFrame
                    df = pd.DataFrame(data)

                    # (a) Scatter plot and correlation coefficient
                    plt.figure(figsize=(10, 6))
                    plt.scatter(df['Size (acres)'], df['Visitors (millions)'])
                    plt.title('National Parks: Size vs. Visitors')
                    plt.xlabel('Size (acres)')
                    plt.ylabel('Visitors (millions)')
                    plt.show()
                    correlation, _ = pearsonr(df['Size (acres)'], df['Visitors (millions)'])
                    print(f'Correlation coefficient: {correlation:.2f}')

                    # (b) Identify unusual park and recalculate correlation
                    unusual_park = df.loc[df['Visitors (millions)'].idxmax()]
                    print(f'Unusual park: {unusual_park["National Park"]}')
                    df_dropped = df.drop(df['Visitors (millions)'].idxmax())
                    correlation_dropped, _ = pearsonr(df_dropped['Size (acres)'],df_dropped['Visitors (millions)'])
                    print(f'Correlation coefficient without unusual park: {correlation_dropped:.2f}')

                    # (c) Effect of changing size units
                    # Convert acres to square miles (1 acre = 0.0015625 square miles)
                    df['Size (sq miles)'] = df['Size (acres)'] * 0.0015625
                    correlation_sq_miles, _ = pearsonr(df['Size (sq miles)'], df['Visitors(millions)'])
                    print(f'Correlation coefficient with size in square miles:{correlation_sq_miles:.2f}')
                    print("The correlation coefficient would not change if size were measured in square miles instead of acres.")
                    print("This is because correlation is a measure of linear relationship between two variables, and the scale of measurement does not affect the linear relationship.")"""
        return code

    if lab == 'mdalab5':
        code =   """
                    ## Linear Regression

                    import numpy as np
                    import pandas as pd
                    import sklearn
                    from sklearn.model_selection import train_test_split
                    from sklearn import linear_model
                    from sklearn.linear_model import LinearRegression
                    from sklearn import metrics
                    from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score

                    df = pd.read_excel('/content/drive/MyDrive/Colab Notebooks/MDA/DATA/DATA/cars.xlsx')
                    x= df[['Weight','Volume']]
                    y = df['CO2']
                    df.head()

                    x = pd.concat([pd.Series(1,index = x.index, name='00'),x],axis = 1)
                    x.head()

                    beta =np.linalg.inv((x.transpose().dot(x))).dot(x.transpose()).dot(y)
                    print(len(x))
                    print(beta)
                    p1 = input("Enter the Vol: ")
                    p2 = input("Enter the weight: ")
                    print(np.array([1,int(p1),int(p2)]).dot(beta))

                    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=100)
                    y_train.shape

                    reg_model = linear_model.LinearRegression()
                    reg_model = LinearRegression().fit(x_train,y_train)

                    print('Intercept: ',reg_model.intercept_)
                    list(zip(x,reg_model.coef_))

                    y_pred = reg_model.predict(x_test)
                    x_pred = reg_model.predict(x_train)

                    print("Prediction for test set:{}".format(y_pred))

                    reg_model_diff = pd.DataFrame({"Actual value":y_test,"Predicted Value":y_pred})
                    reg_model_diff

                    mae=metrics.mean_absolute_error(y_test,y_pred)
                    mse=metrics.mean_squared_error(y_test,y_pred)
                    r2=np.sqrt(metrics.mean_squared_error(y_test,y_pred))
                    print('Mean Absolute Error: ',mae)
                    print('Mean Square Error: ',mse)
                    print('Root Mean Square Error: ',r2)"""
        return code
        
    if lab == 'mdalab6':
        code =   """# Test the Hypothesis: Evaluate T^2 Test

                    import numpy as np
                    from scipy.stats import f, chi2, t

                    def compute_T_square(X, mu_0):
                        n = X.shape[0] # Sample size
                        # Calculate the sample mean vector
                        meanVec = np.mean(X, axis=0)
                        # Calculate the sample covariance matrix
                        S = np.cov(X, rowvar=False)
                        # Compute the T^2 statistic
                        diff = meanVec - mu_0.flatten() # Ensure mu_0 is a 1D array
                        T_squared = n * diff.dot(np.linalg.inv(S)).dot(diff)
                        return T_squared
                    def compute_tabulated_value(X, alpha):
                        n, p = X.shape
                        if n - p > 40:
                        # large sample
                        tab_value = chi2.ppf(1 - alpha, p)
                        else:
                            tab_value = f.ppf(1 - alpha, p, n - p) * ((n - 1) * p / (n - p))
                        return tab_value

                    def make_decision(computed_T_square, table_value):
                        if computed_T_square >= table_value:
                        result = "Reject the null hypothesis"
                        else:
                        result = "Fail to reject the null hypothesis"
                        return result

                    def compute_confidence_interval(X, alpha=0.05):
                        n, p = X.shape # Sample size and number of features
                        # Calculate the sample mean vector
                        meanVec = np.mean(X, axis=0)
                        # Calculate the sample covariance matrix
                        S = np.cov(X, rowvar=False)
                        # Compute the critical value for T-distribution
                        critical_value = t.ppf(1 - alpha/2, df=n - 1)
                        # Compute the standard error
                        standard_error = np.sqrt(np.diag(S) / n)
                        # Constructing the confidence intervals
                        confidence_intervals = []
                        for i in range(p):
                            margin_of_error = critical_value * standard_error[i]
                            ci_lower = meanVec[i] - margin_of_error
                            ci_upper = meanVec[i] + margin_of_error
                            confidence_intervals.append((ci_lower, ci_upper))
                        return confidence_intervals

                    # Example usage
                    X = np.array([[2, 12], [8, 9], [6, 9], [8, 10]])
                    mu_0 = np.array([5, 10]) # Hypothesized mean vector
                    alpha = 0.05
                    T_squared = compute_T_square(X, mu_0)
                    tab_value = compute_tabulated_value(X, alpha)
                    decision = make_decision(T_squared, tab_value)
                    conf_intervals = compute_confidence_interval(X, alpha)
                    print(f"T-squared statistic: {T_squared}")
                    print(f"Tabulated value: {tab_value}")
                    print(f"Decision: {decision}")
                    print("Confidence Intervals:", conf_intervals)"""
        return code
        
    if lab == 'mdalab7':
        code =   """
                    ## MNOVA

                    !pip install statsmodels

                    import pandas as pd
                    from statsmodels.multivariate.manova import MANOVA

                    url = 'https://vincentarelbundock.github.io/Rdatasets/csv/datasets/iris.csv'
                    df = pd.read_csv(url, index_col=0)
                    df.columns = df.columns.str.replace(".", "_")
                    df.head()

                    maov = MANOVA.from_formula('Sepal_Length + Sepal_Width + Petal_Length + Petal_Width ~ Species', data=df)
                    print(maov.mv_test())"""
        return code
        
    if lab == 'mdalab8':
        code =   """
                    ## PCA

                    import numpy as np
                    import pandas as pd
                    import seaborn as sns
                    from tqdm import tqdm
                    import matplotlib.pyplot as plt
                    import matplotlib.cm as cm
                    from sklearn.decomposition import PCA
                    import scipy.cluster.hierarchy as sch
                    import matplotlib.pyplot as plt
                    import seaborn as sns
                    from sklearn.preprocessing import StandardScaler

                    wine_data = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/MDA/DATA/DATA/wine.csv")
                    wine_data.head()

                    # Create a figure with the desired size
                    plt.figure(figsize=(12,10))
                    # Create a subplot
                    f,ax = plt.subplots()
                    # Create the heatmap
                    sns.heatmap(wine_data.corr(),annot=True,linewidth = 0.5,fmt = ".1f",ax=ax)
                    # Show the plot
                    plt.show()

                    standard_scalar = StandardScaler()
                    std_wine = standard_scalar.fit_transform(wine_data)
                    std_wine.shape

                    pca_var = PCA()
                    pca_var.fit(std_wine)
                    #plot
                    plt.figure(figsize=(10,5))
                    xi = np.arange(1,1 + std_wine.shape[1],step = 1)
                    yi = np.cumsum(pca_var.explained_variance_ratio_)
                    plt.plot(xi,yi,marker='o',linestyle="--",color='b')

                    var = pca_var.explained_variance_ratio_
                    var

                    plt.bar(range(1,len(var) + 1),var)
                    plt.xlabel("No of components", fontweight="bold", fontsize=16)
                    plt.ylabel("Variance", fontweight="bold", fontsize=16)
                    plt.title("Explained Variance by each component", fontweight="bold", fontsize=16)
                    plt.show()

                    var1 = np.cumsum(np.round(var,decimals=4)*100)
                    var1

                    pca = PCA(n_components=3)
                    pca_std = pca.fit_transform(std_wine)
                    pca_std_wine = pd.DataFrame(data = pca_std,columns = ['PC1','PC2','PC3'])
                    print(pca_std_wine.shape)
                    pca_std_wine.head()

                    import numpy as np
                    from sklearn.decomposition import PCA

                    # Assuming 'std_wine' is your standardized dataset
                    pca = PCA(n_components=3)
                    pca_std = pca.fit_transform(std_wine)
                    # Calculate the covariance matrix
                    covariance_matrix = np.cov(std_wine.T)
                    # Perform eigendecomposition
                    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)
                    # Sum the eigenvalues
                    total_variance = np.sum(eigenvalues)
                    print(f"Eigenvalues (lambda): {eigenvalues}")
                    print(f"Total variance: {total_variance}")

                    import numpy as np
                    from sklearn.decomposition import PCA
                    import matplotlib.pyplot as plt
                    # Assuming 'std_wine' is your standardized dataset
                    pca = PCA(n_components=3) # Set maximum number of components to 5
                    pca.fit(std_wine)
                    # Calculate cumulative explained variance
                    cumulative_variance_explained = np.cumsum(pca.explained_variance_ratio_)
                    # Find the number of components needed for 80% variance
                    n_components = np.argmax(cumulative_variance_explained >= 0.8) + 1
                    print(f"Number of components needed for 80% variance: {n_components}")
                    # Apply PCA with the determined number of components
                    pca = PCA(n_components=n_components)
                    pca_std = pca.fit_transform(std_wine)

                    # Create DataFrame for the transformed data
                    pca_std_wine = pd.DataFrame(data=pca_std, columns=[f'PC{i+1}' for i in range(n_components)])
                    print(pca_std_wine.shape)
                    print(pca_std_wine.head())"""
        return code
        
    if lab == 'mdalab9':
        code =   """
                    ## Factor Analysis

                    !pip install factor-analyzer

                    import numpy as np
                    import pandas as pd
                    from factor_analyzer import FactorAnalyzer
                    import matplotlib.pyplot as plt
                    df=pd.read_csv('/content/drive/MyDrive/Colab Notebooks/MDA/DATA/DATA/flight.csv')
                    df.head()

                    df.dropna(inplace=True)
                    df1=df.drop(columns=['Unnamed: 0'])
                    print(df1.shape)
                    df1.head()

                    coldrop=['Gender','Customer Type','Type of Travel','Class','Age','Flight Distance','Departure Delay in Minutes','Arrival Delay in Minutes','satisfaction']
                    df2=df1.drop(columns=coldrop)
                    df2.head()
                    df3=df2.drop(columns=['id'])
                    df3.head()

                    from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
                    chi_square_value,p_value=calculate_bartlett_sphericity(df3)
                    chi_square_value, p_value

                    from factor_analyzer.factor_analyzer import calculate_kmo
                    kmo_all,kmo_model=calculate_kmo(df3)
                    kmo_model

                    ncols=df3.shape[1]
                    fa=FactorAnalyzer(n_factors=ncols,rotation=None)
                    fa.fit(df3)

                    ev,_=fa.get_eigenvalues()
                    ev

                    plt.scatter(range(1,ncols+1),ev)
                    plt.plot(range(1,ncols+1),ev)
                    plt.title('Scree Plot')
                    plt.xlabel('Factors')
                    plt.ylabel('Eigenvalue')
                    plt.grid()
                    plt.show()

                    nfactors=5
                    colnames=["F"+str(i) for i in range(1,nfactors+1)]
                    fa=FactorAnalyzer(n_factors=nfactors,rotation='varimax')
                    fa.fit(df3)
                    loadings=pd.DataFrame(fa.loadings_,index=df3.columns,columns=colnames)
                    loadings.head().round(2)

                    communalities=pd.DataFrame(fa.get_communalities(),index=df3.columns,columns=['Communalities'])
                    communalities.head().round(2)

                    var=np.diag(df3.cov())
                    spvar=var-np.array(communalities['Communalities'])
                    sp_var=pd.DataFrame(spvar,index=df3.columns,columns=['Specific Variance'])
                    sp_var.head().round(2)

                    facvar=pd.DataFrame(fa.get_factor_variance(),index=['Variance/SS␣Loadings','Proportion Var','Cumulative Var'],columns=colnames)
                    facvar.head().round(2)"""
        return code
        
    if lab == 'mdalab10':
           code =    """
                        ## K-means Clustering

                        import numpy as np
                        import pandas as pd
                        import matplotlib.pyplot as plt
                        import seaborn as sns

                        df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/MDA/DATA/DATA/Live.csv')
                        df.head()

                        df.isnull().sum()

                        df.drop(['Column1', 'Column2', 'Column3', 'Column4'], axis=1, inplace=True)

                        # view the labels in the variable
                        df['status_id'].unique()
                        # view how many different types of variables are there
                        len(df['status_id'].unique())

                        df.drop(['status_id', 'status_published'], axis=1, inplace=True)

                        X = df
                        y = df['status_type']

                        from sklearn.preprocessing import LabelEncoder
                        le = LabelEncoder()
                        X['status_type'] = le.fit_transform(X['status_type'])
                        y = le.transform(y)

                        cols = X.columns
                        from sklearn.preprocessing import MinMaxScaler
                        ms = MinMaxScaler()
                        X = ms.fit_transform(X)
                        X = pd.DataFrame(X, columns=[cols])

                        from sklearn.cluster import KMeans
                        kmeans = KMeans(n_clusters=2, random_state=0)
                        kmeans.fit(X)

                        kmeans.cluster_centers_
                        kmeans.inertia_

                        # Check quality of weak classification by the model
                        labels = kmeans.labels_
                        # check how many of the samples were correctly labeled
                        correct_labels = sum(y == labels)
                        print("Result: %d out of %d samples were correctly labeled." % (correct_labels,y.size))

                        print('Accuracy score: {0:0.2f}'. format(correct_labels/float(y.size)))

                        from sklearn.cluster import KMeans
                        cs = []
                        for i in range(1, 11):
                        kmeans = KMeans(n_clusters = i, init = 'k-means++', max_iter = 300, n_init= 10, random_state = 0)
                        kmeans.fit(X)
                        cs.append(kmeans.inertia_)

                        plt.plot(range(1, 11), cs)
                        plt.title('The Elbow Method')
                        plt.xlabel('Number of clusters')
                        plt.ylabel('CS')
                        plt.show()

                        from sklearn.cluster import KMeans
                        kmeans = KMeans(n_clusters=2,random_state=0)
                        kmeans.fit(X)
                        labels = kmeans.labels_
                        # check how many of the samples were correctly labeled
                        correct_labels = sum(y == labels)
                        print("Result: %d out of %d samples were correctly labeled." % (correct_labels,y.size))
                        print('Accuracy score: {0:0.2f}'. format(correct_labels/float(y.size)))

                        kmeans = KMeans(n_clusters=3, random_state=0)
                        kmeans.fit(X)
                        # check how many of the samples were correctly labeled
                        labels = kmeans.labels_
                        correct_labels = sum(y == labels)
                        print("Result: %d out of %d samples were correctly labeled." % (correct_labels,y.size))
                        print('Accuracy score: {0:0.2f}'. format(correct_labels/float(y.size)))

                        kmeans = KMeans(n_clusters=4, random_state=0)
                        kmeans.fit(X)
                        # check how many of the samples were correctly labeled
                        labels = kmeans.labels_
                        correct_labels = sum(y == labels)
                        print("Result: %d out of %d samples were correctly labeled." % (correct_labels,y.size))
                        print('Accuracy score: {0:0.2f}'. format(correct_labels/float(y.size)))"""
           return code
    
    if lab == 'mdalab11':
        code =   """
                    ## MANOVA manual and Wilks Lambda

                    import pandas as pd
                    import numpy as np
                    import seaborn as sns
                    import statsmodels
                    from statsmodels.multivariate.manova import MANOVA

                    data = sns.load_dataset('iris')
                    data.head(5)

                    dependent_vars = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
                    independent_vars = 'species'

                    manova_model = MANOVA.from_formula(f'{"+".join(dependent_vars)} ~ {independent_vars}',data=data)
                    manova_result = manova_model.mv_test()
                    print(manova_result)

                    X = data[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']].values
                    y = data['species'].values

                    # Unique groups
                    groups = np.unique(y)
                    groups

                    # Calculate the mean vectors for each group
                    mean_vectors = []
                    for group in groups:
                        mean_vectors.append(np.mean(X[y == group], axis=0))
                    print("Mean vectors:", mean_vectors)
                    # Calculate the overall mean vector
                    overall_mean = np.mean(X, axis=0)
                    print("Overall mean:",overall_mean)

                    # Calculate the within-group scatter matrix
                    S_W = np.zeros((4, 4))
                    for group, mean_vec in zip(groups, mean_vectors):
                        group_scatter = np.cov(X[y == group].T) * (X[y == group].shape[0] - 1)
                        S_W += group_scatter

                    # Calculate the between-group scatter matrix
                    S_B = np.zeros((4, 4))
                    for mean_vec in mean_vectors:
                        n = X[y == group].shape[0]
                        mean_diff = (mean_vec - overall_mean).reshape(4, 1)
                        S_B += n * (mean_diff).dot(mean_diff.T)

                    # Calculate Wilks' lambda
                    lambda_val = np.linalg.det(S_W) / np.linalg.det(S_W + S_B)
                    print(f"Wilks' lambda: {lambda_val}")"""
        return code
        
    if lab == 'mdalab12':
        code =   """
                    ## Logistic Regression

                    import pandas as pd
                    import numpy as np
                    import seaborn as sns
                    import statsmodels
                    from statsmodels.multivariate.manova import MANOVA

                    data = sns.load_dataset('iris')
                    data.head(5)

                    dependent_vars = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
                    independent_vars = 'species'

                    manova_model = MANOVA.from_formula(f'{"+".join(dependent_vars)} ~ {independent_vars}',data=data)
                    manova_result = manova_model.mv_test()
                    print(manova_result)

                    X = data[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']].values
                    y = data['species'].values

                    # Unique groups
                    groups = np.unique(y)
                    groups

                    # Calculate the mean vectors for each group
                    mean_vectors = []
                    for group in groups:
                        mean_vectors.append(np.mean(X[y == group], axis=0))
                    print("Mean vectors:", mean_vectors)
                    # Calculate the overall mean vector
                    overall_mean = np.mean(X, axis=0)
                    print("Overall mean:",overall_mean)

                    # Calculate the within-group scatter matrix
                    S_W = np.zeros((4, 4))
                    for group, mean_vec in zip(groups, mean_vectors):
                        group_scatter = np.cov(X[y == group].T) * (X[y == group].shape[0] - 1)
                        S_W += group_scatter

                    # Calculate the between-group scatter matrix
                    S_B = np.zeros((4, 4))
                    for mean_vec in mean_vectors:
                        n = X[y == group].shape[0]
                        mean_diff = (mean_vec - overall_mean).reshape(4, 1)
                        S_B += n * (mean_diff).dot(mean_diff.T)

                    # Calculate Wilks' lambda
                    lambda_val = np.linalg.det(S_W) / np.linalg.det(S_W + S_B)
                    print(f"Wilks' lambda: {lambda_val}")"""
        return code
        
    else:
        return "The correct format: eg:- mdalab1, please check the format of input"
