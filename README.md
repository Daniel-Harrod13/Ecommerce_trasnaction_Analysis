# Data Cleaning for E-commerce Analysis

## About the Dataset

### Context

E-commerce has emerged as a pivotal channel for business development, enabling companies to establish a broader market presence through cost-effective and efficient distribution channels. This shift has fundamentally altered consumer behavior, with many individuals opting to shop online using computers or smart devices, facilitating convenient home deliveries.

### Content

This dataset comprises **500,000 rows** and **8 columns**, representing one year of sales transactions from a UK-based e-commerce (online retail) business. The London-based shop specializes in selling gifts and homewares for both adults and children through its website since 2007. The customer base is diverse, including:

- **Individual Consumers**: Making direct purchases for personal use.
- **Small Businesses**: Purchasing in bulk to resell through retail outlets.

#### Column Descriptions

1. **TransactionNo (categorical)**:  
   - A six-digit unique identifier for each transaction.
   - The prefix “C” denotes a cancellation.

2. **Date (numeric)**:  
   - The date when the transaction occurred.

3. **ProductNo (categorical)**:  
   - A five or six-digit unique identifier for each product.

4. **Product (categorical)**:  
   - The name of the product/item sold.

5. **Price (numeric)**:  
   - The unit price of the product in pound sterling (£).

6. **Quantity (numeric)**:  
   - The number of units purchased in each transaction.
   - Negative values indicate canceled transactions.

7. **CustomerNo (categorical)**:  
   - A five-digit unique identifier for each customer.

8. **Country (categorical)**:  
   - The country where the customer is located.

**Note:** A small percentage of transactions are cancellations, primarily due to products being out of stock. Customers typically cancel orders to ensure that all desired products are delivered simultaneously.

### Inspiration

In today’s competitive business landscape, information is a critical asset. The ability to acquire, store, and utilize data effectively can significantly influence a company’s success. Data analysis serves as a cornerstone for extracting valuable insights that drive informed decision-making.

**Objectives:**

Analyze this dataset to address the following questions:

1. **Sales Trend Analysis:**  
   - How did sales evolve over the months?

2. **Product Popularity:**  
   - What are the most frequently purchased products?

3. **Customer Purchase Behavior:**  
   - How many products do customers typically purchase in each transaction?

4. **Profitability Segmentation:**  
   - Which customer segments are the most profitable?

5. **Strategic Recommendations:**  
   - Based on the findings, what strategies can be recommended to enhance business profitability?

---

