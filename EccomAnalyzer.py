import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import plotly.express as px

class EcommerceAnalyzer:
    def __init__(self, data_path):
        """Initialize the analyzer with the path to the sales data."""
        self.df = pd.read_csv(data_path)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.preprocess_data()
    
    def preprocess_data(self):
        """Clean and prepare the data for analysis."""
        # Remove any negative quantities or prices
        self.df = self.df[self.df['Quantity'] > 0]
        self.df = self.df[self.df['Price'] > 0]
        
        # Calculate total amount per transaction
        self.df['Total_Amount'] = self.df['Quantity'] * self.df['Price']
        
        # Extract month and year
        self.df['Month_Year'] = self.df['Date'].dt.to_period('M')
        
        # Add geographic dimension
        self.df['Region'] = self.df['Country'].astype('category')
    
    def analyze_sales_trends(self):
        """Analyze monthly sales trends."""
        monthly_sales = self.df.groupby(['Month_Year', 'Country']).agg({
            'Total_Amount': 'sum',
            'TransactionNo': 'nunique'
        }).reset_index()
        monthly_sales['Month_Year'] = monthly_sales['Month_Year'].astype(str)
        
        return monthly_sales
    
    def analyze_product_popularity(self, top_n=10):
        """Identify top selling products."""
        product_sales = self.df.groupby(['ProductNo', 'ProductName']).agg({
            'Quantity': 'sum',
            'Total_Amount': 'sum',
            'Country': 'nunique'  # Number of countries where product is sold
        }).reset_index()
        
        return product_sales.nlargest(top_n, 'Total_Amount')
    
    def analyze_purchase_behavior(self):
        """Analyze items per transaction distribution."""
        items_per_transaction = self.df.groupby(['TransactionNo', 'Country']).agg({
            'Quantity': 'sum',
            'Total_Amount': 'sum',
            'ProductNo': 'nunique'  # Number of unique products
        }).reset_index()
        
        return {
            'avg_items': items_per_transaction['ProductNo'].mean(),
            'median_items': items_per_transaction['ProductNo'].median(),
            'avg_amount': items_per_transaction['Total_Amount'].mean(),
            'distribution': items_per_transaction
        }
    
    def segment_customers(self, n_clusters=4):
        """Segment customers based on RFM analysis with geographical consideration."""
        current_date = self.df['Date'].max()
        
        # Calculate RFM metrics
        rfm = self.df.groupby('CustomerNo').agg({
            'Date': lambda x: (current_date - x.max()).days,  # Recency
            'TransactionNo': 'nunique',  # Frequency
            'Total_Amount': 'sum',  # Monetary
            'Country': lambda x: x.mode()[0]  # Most common country
        }).reset_index()
        
        rfm.columns = ['CustomerNo', 'Recency', 'Frequency', 'Monetary', 'PrimaryCountry']
        
        # Scale the features
        scaler = StandardScaler()
        rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])
        
        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        rfm['Segment'] = kmeans.fit_predict(rfm_scaled)
        
        return rfm
    
    def analyze_geographic_distribution(self):
        """Analyze sales patterns across different countries."""
        geo_analysis = self.df.groupby('Country').agg({
            'Total_Amount': 'sum',
            'CustomerNo': 'nunique',
            'TransactionNo': 'nunique',
            'ProductNo': 'nunique'
        }).reset_index()
        
        return geo_analysis
    
    def generate_visualizations(self):
        """Generate key visualizations for the analysis."""
        # Sales trend visualization
        monthly_sales = self.analyze_sales_trends()
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=monthly_sales, x='Month_Year', y='Total_Amount', hue='Country')
        plt.title('Monthly Sales Trend by Country')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Product popularity visualization
        top_products = self.analyze_product_popularity()
        plt.figure(figsize=(12, 6))
        sns.barplot(data=top_products, x='Total_Amount', y='ProductName')
        plt.title('Top 10 Products by Revenue')
        plt.tight_layout()
        
        # Geographic distribution
        geo_analysis = self.analyze_geographic_distribution()
        plt.figure(figsize=(10, 6))
        sns.barplot(data=geo_analysis, x='Country', y='Total_Amount')
        plt.title('Sales Distribution by Country')
        plt.xticks(rotation=45)
        plt.tight_layout()
    
    def generate_report(self):
        """Generate a comprehensive analysis report."""
        report = {
            'sales_trends': self.analyze_sales_trends(),
            'top_products': self.analyze_product_popularity(),
            'purchase_behavior': self.analyze_purchase_behavior(),
            'customer_segments': self.segment_customers(),
            'geographic_analysis': self.analyze_geographic_distribution()
        }
        
        return report

# Example usage
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = EcommerceAnalyzer('/Users/danielharrod/Ecommerce_transaction_Analysis/data/Sales_Transaction_Cleaned.csv')
    
    # Generate comprehensive report
    report = analyzer.generate_report()
    
    # Generate visualizations
    analyzer.generate_visualizations()
    
    # Print key insights
    print("=== E-commerce Analysis Results ===")
    print("\nTop 5 Products by Revenue:")
    print(report['top_products'][['ProductName', 'Total_Amount', 'Quantity']].head())
    
    print(f"\nAverage Products per Transaction: {report['purchase_behavior']['avg_items']:.2f}")
    print(f"Average Transaction Amount: ${report['purchase_behavior']['avg_amount']:.2f}")
    
    print("\nSales by Country:")
    print(report['geographic_analysis'][['Country', 'Total_Amount', 'CustomerNo']].sort_values('Total_Amount', ascending=False))
    
    print("\nCustomer Segments Summary:")
    print(report['customer_segments'].groupby(['Segment', 'PrimaryCountry']).agg({
        'Monetary': 'mean',
        'Frequency': 'mean',
        'Recency': 'mean'
    }).round(2))