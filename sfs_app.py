{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "c89b9201",
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'mlxtend'",
     "output_type": "error",
     "traceback": [
      "\u001b[31m---------------------------------------------------------------------------\u001b[39m",
      "\u001b[31mModuleNotFoundError\u001b[39m                       Traceback (most recent call last)",
      "\u001b[36mCell\u001b[39m\u001b[36m \u001b[39m\u001b[32mIn[1]\u001b[39m\u001b[32m, line 6\u001b[39m\n\u001b[32m      4\u001b[39m \u001b[38;5;28;01mfrom\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[34;01msklearn\u001b[39;00m\u001b[34;01m.\u001b[39;00m\u001b[34;01mlinear_model\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mimport\u001b[39;00m LogisticRegression\n\u001b[32m      5\u001b[39m \u001b[38;5;28;01mfrom\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[34;01msklearn\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mimport\u001b[39;00m datasets\n\u001b[32m----> \u001b[39m\u001b[32m6\u001b[39m \u001b[38;5;28;01mfrom\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[34;01mmlxtend\u001b[39;00m\u001b[34;01m.\u001b[39;00m\u001b[34;01mfeature_selection\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mimport\u001b[39;00m SequentialFeatureSelector \u001b[38;5;28;01mas\u001b[39;00m SFS\n\u001b[32m      7\u001b[39m \u001b[38;5;28;01mfrom\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[34;01mmlxtend\u001b[39;00m\u001b[34;01m.\u001b[39;00m\u001b[34;01mplotting\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mimport\u001b[39;00m plot_sequential_feature_selection \u001b[38;5;28;01mas\u001b[39;00m plot_sfs\n\u001b[32m      8\u001b[39m \u001b[38;5;28;01mimport\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[34;01mstreamlit\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mas\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[34;01mst\u001b[39;00m\n",
      "\u001b[31mModuleNotFoundError\u001b[39m: No module named 'mlxtend'"
     ]
    }
   ],
   "source": [
    "# sequential feature selector app in streamlit:\n",
    "import pandas as pd\n",
    "from sklearn.linear_model import LinearRegression\n",
    "from sklearn.linear_model import LogisticRegression\n",
    "from sklearn import datasets\n",
    "from mlxtend.feature_selection import SequentialFeatureSelector as SFS\n",
    "from mlxtend.plotting import plot_sequential_feature_selection as plot_sfs\n",
    "import streamlit as st\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "\n",
    "st.title(\"SFS!\")\n",
    "input_data_url = st.text_input(\"Enter the URL to the dataset (csv file format). Ensure all variables are numbers\")\n",
    "if \".csv\" not in input_data_url:\n",
    "    st.write(\"No data\")\n",
    "    st.stop()\n",
    "\n",
    "df = pd.read_csv(input_data_url)\n",
    "\n",
    "col1, col2 = st.columns(2)\n",
    "\n",
    "chosen_y = col1.selectbox(\"Choose a dependent variable:\", df.columns)\n",
    "if chosen_y == None:\n",
    "    col1.write(\"Have one variable as the dependent\")\n",
    "    st.stop()\n",
    "\n",
    "y = df.loc[:,chosen_y]\n",
    "col1.write(y.head())\n",
    "\n",
    "chosen_X = col2.multiselect(\"Choose independent variables:\", df.drop(columns = chosen_y).columns)\n",
    "\n",
    "X = df.loc[:,chosen_X]\n",
    "\n",
    "col2.write(X.head())\n",
    "\n",
    "if len(chosen_X) <= 1:\n",
    "    col2.write(\"Please select more than one column\")\n",
    "    st.stop()\n",
    "\n",
    "col1, col2 = st.columns(2)\n",
    "k = col1.slider(\"Select the number of important features needed:\", 1,\n",
    "              X.shape[1], X.shape[1])\n",
    "\n",
    "reg_or_class_option = col2.selectbox(\"Regression or Classification?\", options=['regression', 'classification'])\n",
    "\n",
    "lr, scoring = (LinearRegression(), 'neg_root_mean_squared_error') if reg_or_class_option == 'regression' else (LogisticRegression(), 'accuracy')\n",
    "# lr, scoring = (LinearRegression(), 'neg_root_mean_squared_error')\n",
    "\n",
    "sfs = SFS(lr,\n",
    "          k_features=k,\n",
    "          forward=True,\n",
    "          scoring=scoring,\n",
    "          cv=0)\n",
    "\n",
    "sfs = sfs.fit(X, y)\n",
    "\n",
    "sfs_metric = pd.DataFrame.from_dict(sfs.get_metric_dict()).T\n",
    "st.write(\"Best features are:\")\n",
    "st.write(sfs_metric.iloc[-1,3])\n",
    "st.line_chart(data = sfs_metric, y = 'avg_score')\n",
    "\n",
    "st.write(sfs_metric)\n",
    "\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
