import requests
#url="https://openlibrary.org/search.json?q=the+lord+of+the+rings"
url="https://openlibrary.org/search.json?q="
book=input("Enter book name:")
joinBook = "+".join(book.split())
fullUrl=url+joinBook
 
response=requests.get(fullUrl)
data=response.json()
english_books=[]
print("Total books found:",data["numFound"])
for book in data["docs"]:
    if "language" in book and "eng" in book["language"]:
        english_books.append(book)
print("Nmber of books available in English:",len(english_books))
 
# first_book = data["docs"][0]
# print(first_book.keys())
for i in english_books[:10]:
    print("-",i.get("title","unknown title"))
for i in english_books[:1]:
    print(i)
