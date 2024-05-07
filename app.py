from flask import Flask, render_template,request
import pickle
import jinja2
import numpy as np

data_df=pickle.load(open('book.pkl','rb'))
pivot_table=pickle.load(open('pivot_table.pkl','rb'))
similarity_score=pickle.load(open('similarity_score.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           image=list(data_df['Image-URL-M'].values),
                           book_name=list(data_df['Book-Title'].values),
                           publisher=list(data_df['Publisher'].values),
                            author=list(data_df['Book-Author'].values),
                           votes=list(data_df['num-Rating'].values),
                           rating=list(data_df['avg-Rating'].values),
                           )  

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input=request.form.get('user_input')
    index= np.where(pivot_table.index==user_input)[0][0]
    similar_book = sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:6]

    data=[]
    for i in similar_book:
      item=[]
      temp_df = books[books['Book-Title'] == pivot_table.index[i[0]]]
      item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
      item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
      item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
      data.append(item)

      print(data)
    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)
