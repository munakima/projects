## 📚 Projects

This repository contains a collection of my C# and Python projects.
Here are the projects included in this repository:

### :computer: C# Projects

This list shows a collection of my C# projects. Each project is a standalone application or script that demonstrates my Python coding skills and understanding of technologies and frameworks.

#### :ticket: [eTickets System](https://github.com/munakima/projects/tree/main/eTickets%20system)

eTickets is a web application that allows users to browse movies, book tickets and manage the database. It is built using the following technologies:    
- C#, .NET Core, ASP.NET Core MVC, Entity Framework Core, Razor,HTML, CSS, JavaScript, Microsoft SQL Server, EF Code First, Repository Pattern, Unit of Work Pattern, Services Pattern, Dependency Injection, Unit Testing. 

#### :ticket: [EDTrackingService](https://github.com/munakima/EDTrackingService)

EDTrackingService is a package delivery tracking system designed to provide end-to-end visibility of package delivery operations. The system is built on a multi-layered architecture consisting of a Data Access Layer (DAL), Data Access Layer API (DAL_API), Business Logic Layer (BLL), Business Logic Layer API (BLL_API), Data Transfer Object (DTO) and User Interface (UI) layer.
eTickets is a web application that allows users to browse movies, book tickets and manage the database. It is built using the following technologies:
- C#, .NET Framework, ASP.NET, ASP.NET MVC, Entity Framework, HTML, Razor, CSS, JavaScript,  EF Code First, Repository Pattern, Facade Pattern, gateway Pattern, Dependency Injection(Ninject), Unit Testing.

#### :fork_and_knife: [ChopsticksApp](https://github.com/munakima/ChopsticksApp)

A web application for managing restaurant orders would allow customers to book a table, place take-away orders, and view the restaurant's menu online. The application would also enable restaurant staff to manage orders, manage data. Customers would be able to create an account, browse the menu, place orders. 

#### :ticket: [EasvTickets](https://github.com/munakima/EasvTickets)

The web application is designed for the EASV academy, allowing users to browse upcoming events, select and book tickets for their desired events. Once a user books a ticket, a unique QR code is generated and added to a PDF ticket, which can be downloaded and used as a ticket for the event. 

### 🐍 Python Projects

This list shows a collection of my Python projects. Each project is a standalone application or script that demonstrates my Python coding skills and understanding of various Python libraries and frameworks.

#### :dna: [ProteinDB](./https://github.com/munakima/projects/tree/main/ProteinDB)

A Python system for cleaning up raw data and extracting information from 
[Protein Data Bank](https://www.rcsb.org/docs/programmatic-access/file-download-services) and [AlphaFold Protein](https://alphafold.ebi.ac.uk/download) Structure Databases. It will help predict protein folding, protein 3D structures and protein-protein interactions.


#### 🩺 [Breast Cancer Wisconsin (Diagnostic)](./Breast_Cancer_Wisconsin_(Diagnostic).ipynb)

This project is a machine learning model that predicts whether a tumor is malignant or benign based on various features extracted from medical images of breast tissue. The model is trained on the [Breast Cancer Wisconsin (Diagnostic) dataset](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)) using the [scikit-learn](https://scikit-learn.org/) machine learning library.

- Technologies Used: Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn
- Data Cleaning and Exploration: Checking for missing values, Checking for duplicate data, Removing the "Unnamed" column, Converting "diagnosis" to category type, Removing outliers

After exploring the data, I found that removing outliers using Interquartile range (IQR) significantly improved the accuracy of the model. Using my get_outlier and get_outlier_by_weight functions, I was able to remove the outliers and achieve an accuracy of 1.0 with the RandomForestClassifier algorithm. 

#### 💰 [Medical Cost Estimation](./Medical_Cost_Estimation.ipynb)

This project is a data analysis and visualization project that explores the [Medical Cost Personal Datasets](https://www.kaggle.com/mirichoi0218/insurance) on Kaggle. The project aims to answer questions like "What factors contribute to higher medical costs?" using Python data analysis and visualization libraries like [pandas](https://pandas.pydata.org/) and [matplotlib](https://matplotlib.org/).

The project starts with loading the dataset and preparing it for analysis. Missing values and duplicate data are checked, and then the data is analyzed and visualized. The correlation between various features and the medical cost charged is determined through feature selection, with smoking habits being the most important feature.

The data is then cleaned by removing outliers, I implemented a strategy for outlier removal that involved grouping the data based on smoking status, age, and charges. Outliers were then identified and removed separately for smokers and non-smokers. For smokers, I removed individuals at a certain age whose medical costs exceeded those of the oldest individuals in the dataset. The same criterion was applied for non-smokers to identify and remove outliers. 

Feature encoding is used to transform categorical variables into numerical variables for use in machine learning algorithms. Three regression algorithms, namely Linear Regression, XGBRegressor, and RandomForestRegressor, are trained and evaluated. The RandomForestRegressor algorithm performs the best with an R-squared value of 0.9698, indicating that it can predict the medical cost charged by healthcare providers with high accuracy.

##### Data analysis 
What factors contribute to higher medical costs?
- The correlation between the features looks like:

| Feature 1 | Feature 2 | Correlation Coefficient|
|-----------|-----------|------------------------|
| charges   | charges   | 1.000000               |
| charges   | smoker    | 0.787251               |
| charges   | age       | 0.299008               |
| charges   | bmi       | 0.198341               |
| charges   | children  | 0.067998               |
| charges   | sex       | 0.057292               |
| charges   | region    | 0.006208               |

Based on the correlation coefficients, the factors that contribute the most to higher medical costs are smoking, age, and BMI. Specifically, smoking has the highest correlation with medical costs (0.787251), meaning that smokers tend to have higher medical costs than non-smokers. Age also has a moderate positive correlation (0.299008), indicating that as people get older, their medical costs tend to increase. 

BMI has a weak positive correlation (0.198341), but after conducting a separate analysis on individuals who smoke, it was found that as the BMI increases, there is a corresponding increase in medical costs. However, this correlation was not observed in non-smokers. 

On the other hand, sex and region seem to have a negligible impact on medical costs, according to the low correlation coefficients (0.057292 and 0.006208, respectively).

#### 🩺 [Pneumonia Classification](./Pneumonia_Classification.ipynb)

This project is a deep learning model that classifies chest X-ray images into normal and pneumonia cases. The model is trained on the [Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia) dataset using the [Keras](https://keras.io/) deep learning library.

This project implementing a convolutional neural network (CNN) for classifying pneumonia images using TensorFlow and Keras. The code imports necessary libraries, such as os, shutil, and matplotlib, and sets up a data generator for image augmentation. The CNN model is defined with several convolutional layers, spatial dropout, batch normalization, max pooling, and dense layers with sigmoid activation. The model is compiled using the RMSprop optimizer and binary cross-entropy loss. The code also sets up early stopping and saves the trained model weights to files. The training process is performed using the fit method with callbacks for early stopping and validation. Finally, the model is evaluated using the evaluate method, which returns the loss and accuracy on the evaluation dataset.

- The model was compiled using the RMSprop optimizer, binary cross-entropy loss function, and accuracy metric.
- After training on the training dataset, the model achieved a training loss of 0.2440 and a training accuracy of 0.9068.
- The model was evaluated on the validation dataset, and it achieved a loss of 0.3691 and an accuracy of 0.843.    
    

    
Feel free to explore the code and learn more about these projects. If you have any questions or suggestions, please feel free to reach out to me.

Thank you for visiting my Python projects repository! 🙏
