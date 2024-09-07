from bs4 import BeautifulSoup
import requests
import pandas as pd

# Define the URL and headers
url = "http://books.toscrape.com/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# Request the page content
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, "html.parser")

# Find the books section
books = soup.find_all('article', class_='product_pod')

# Initialize lists to store the scraped data
titles = []
prices = []
availability = []
ratings = []
genres = [genre.text.strip() for genre in soup.select('.side_categories ul li a')]

# Loop through each book and extract details
for book in books:
    title = book.h3.a['title']
    price = book.find('p', class_='price_color').text
    avail = book.find('p', class_='instock availability').text.strip()
    rating = book.find('p', class_='star-rating')['class'][1]  # Rating class is like 'One', 'Two', etc.
    
    titles.append(title)
    prices.append(price)
    availability.append(avail)
    ratings.append(rating)

# Create a DataFrame from the lists
df_books = pd.DataFrame({
    'Title': titles,
    'Price': prices,
    'Availability': availability,
    'Rating': ratings
})

# Add genre information (assuming it's the same for all books on the page)
df_books['Genre'] = genres[0]  # This example assumes genre is uniform for the catalog page

# Set the title as the index
df_books.set_index('Title', inplace=True)

# Print the DataFrame
print(df_books.head())

# Export the DataFrame to a CSV file
df_books.to_csv('books_extended.csv')
