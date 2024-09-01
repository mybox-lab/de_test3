import csv
import requests
import matplotlib.pyplot as plt

def read_sales_data(file_path):
    # Скачиваем файл с указанного URL
    response = requests.get(file_path)
    response.raise_for_status()  # Проверяем, успешно ли выполнен запрос

    # Читаем содержимое файла и обрабатываем его как CSV
    sales_data = []
    decoded_content = response.content.decode('utf-8')
    reader = csv.reader(decoded_content.splitlines())
    # Проходим по строкам файла и помещаем данные в словарь
    for row in reader:
        product_name, quantity, price, date = row
        sales_data.append({
            'product_name': product_name,
            'quantity': int(quantity),
            'price': float(price),
            'date': date
        })
    
    return sales_data	
    
def total_sales_per_product(sales_data):
    # Читаем список продаж и формируем словарь, где ключ - название продукта, а значение - общая сумма продаж этого продукта.  
    sales_per_product = {}
    for sale in sales_data:
        product = sale['product_name']
        total_sale = sale['quantity'] * sale['price']
        if product in sales_per_product:
            sales_per_product[product] += total_sale
        else:
            sales_per_product[product] = total_sale
    return sales_per_product
	
def sales_over_time(sales_data):
    # Читаем список продаж и формируем словарь, где ключ - дата, а значение общая сумма продаж за эту дату..  
    sales_by_date = {}
    for sale in sales_data:
        date = sale['date']
        total_sale = sale['quantity'] * sale['price']
        if date in sales_by_date:
            sales_by_date[date] += total_sale
        else:
            sales_by_date[date] = total_sale
    return sales_by_date
	
def analyze_sales(file_path):
    # Формируем список продаж
    sales_data = read_sales_data(file_path)
    
    # Формируем список, общая сумма продаж по продуктам
    sales_per_product = total_sales_per_product(sales_data)
    
    # Формируем список, общая сумма продаж по датам
    sales_by_date = sales_over_time(sales_data)
    
    # Определяем продукт с наибольшей выручкой
    max_product = max(sales_per_product, key=sales_per_product.get)
    print(f'Продажа продукта "{max_product}" имеет наибольшую выручку: {sales_per_product[max_product]}')

    # Определяем день с наибольшей суммой продаж
    max_date = max(sales_by_date, key=sales_by_date.get)
    print(f'"{max_date}" день с наибольшей суммой продаж: {sales_by_date[max_date]}\n')
    
    return sales_per_product, sales_by_date

def plot_sales(sales_per_product, sales_by_date):
    # График общей суммы продаж по каждому продукту
    products = list(sales_per_product.keys())
    sales_values = list(sales_per_product.values())
    max_sales_values = max(sales_values)

    plt.figure(figsize=(7, 5))
    plt.bar(products, sales_values, color='blue')
    plt.xlabel('Продукты')
    plt.ylabel('Общая сумма продаж')
    plt.title('Общая сумма продаж по продуктам')
    plt.xticks(rotation=45, ha='right')
    plt.axhline(max_sales_values, color='r', linestyle='dashed', linewidth=1)
    plt.text(0, max_sales_values, str(max_sales_values))    
    plt.tight_layout()
    plt.show()
    
    # График общей суммы продаж по датам
    dates = list(sales_by_date.keys())
    sales_by_date_values = list(sales_by_date.values())
    max_sales_by_date_values = max(sales_by_date_values)

    plt.figure(figsize=(7, 5))
    plt.plot(dates, sales_by_date_values, marker='o', color='green')
    plt.xlabel('Дата')
    plt.ylabel('Общая сумма продаж')
    plt.title('Общая сумма продаж по датам')
    plt.xticks(rotation=45, ha='right')
    plt.axhline(max_sales_by_date_values, color='r', linestyle='dashed', linewidth=1)  
    plt.text(0, max_sales_by_date_values, str(max_sales_by_date_values))
    plt.tight_layout()
    plt.show()
	
if __name__ == "__main__":
    file_path = 'https://raw.githubusercontent.com/mybox-lab/de_test3/main/sales_data.csv' #URL для скачивания файла 
    sales_per_product, sales_by_date = analyze_sales(file_path)
    plot_sales(sales_per_product, sales_by_date)