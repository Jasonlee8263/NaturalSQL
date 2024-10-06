import sqlite3
import openai
import os

# Initialize OpenAI API
openai.api_key = os.getenv("openai_API_KEY")
# Connect to SQLite database
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

def ask_gpt_for_sql(question):
    response = openai.chat.completions.create(
        model="gpt-4o",  # 사용할 모델 선택 (gpt-3.5-turbo 등도 사용 가능)
        messages=[
            {"role": "system", "content": "You are an assistant that generates SQL queries. Please generate Only SQL query. Also please use syntax that is compatible with SQLite. Use the following variable names: Customers, Orders, MenuItems, OrderItems, CustomerID, Name, Email, OrderID, Date, TotalPrice, MenuItemID, Price, OrderItemID, Quantity."},
            {"role": "user", "content": question}
        ]
    )
    sql_query = response.choices[0].message.content.strip()  # 양쪽 공백 제거
    sql_query = sql_query.replace('```sql\n', '').replace('```', '')  # 불필요한 텍스트 제거
    return sql_query

def execute_sql_query(sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

def friendly_response(results):
    if not results:
        return "No results found."
    results_string = "\n".join(str(row) for row in results)  # 각 결과를 줄 바꿈으로 구분
    response = openai.chat.completions.create(
        model="gpt-4o",  # 사용할 모델 선택 (gpt-3.5-turbo 등도 사용 가능)
        messages=[
            {"role": "system", "content": "You are an assistant that provides a friendly response to SQL query results. If you need to format the results, please do so in a human-readable way. If you need to summarize the results, please do so in a concise manner. If you don't know how to respond, you can say 'I'm not sure.' Is there anything else you want to know? Don’t say things like that. And don’t use technical terms like ‘query.’ Just tell regular people the results."},
            {"role": "user", "content": results_string}
        ]
    )
    # for row in results:
    #     response += f"{row}\n"
    result = response.choices[0].message.content
    return result

def main():
    questions = [
        "What are the names and email addresses of all customers?",
        "Can you provide the order details for a specific customer by their CustomerID?",
        "How many customers have placed orders in the last month?",
        "What is the total revenue generated from all orders placed this year?",
        "Which menu items have a price higher than $20?",
        "Who is the customer with the highest total order value, and what is that value?",
        "What is the average total price of orders placed in the last 2 months?",
        "What is the average price of menu items?"
    ]
    for question in questions:
        print(f"\nAsking: {question}")
        sql_query = ask_gpt_for_sql(question)
        print(f"Generated SQL Query: {sql_query}")
        try:
            results = execute_sql_query(sql_query)
            print(friendly_response(results))
        except sqlite3.Error as e:
            print(f"SQL error: {e}")

if __name__ == "__main__":
    main()