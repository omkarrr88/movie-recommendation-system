import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import json
from Classifier import KNearestNeighbours
from tkinter import ttk
from bs4 import BeautifulSoup
import requests, io
import PIL.Image
from urllib.request import urlopen

# Load data
def create_scrollbar(frame):
    canvas = tk.Canvas(frame)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure("all", scrollregion=canvas.bbox("all")))
    return canvas

with open('movie_data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
with open('movie_titles.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f)
hdr = {'User-Agent': 'Mozilla/5.0'}

def movie_poster_fetcher(imdb_link):
    ## Display Movie Poster
    url_data = requests.get(imdb_link, headers=hdr).text
    s_data = BeautifulSoup(url_data, 'html.parser')
    imdb_dp = s_data.find("meta", property="og:image")
    movie_poster_fetcher = imdb_dp.attrs['content']
    u = urlopen(movie_poster_fetcher)
    raw_data = u.read()
    image = PIL.Image.open(io.BytesIO(raw_data))
    image = image.resize((158, 301), )
    return image

def get_movie_info(link):
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    url_data = requests.get(link, headers=hdr).text
    s_data = BeautifulSoup(url_data, 'html.parser')
    imdb_content = s_data.find("meta", property="og:description")
    movie_descr = imdb_content.attrs['content']
    movie_descr = str(movie_descr).split('.')

    movie_director = movie_descr[0] if len(movie_descr) > 0 else ''
    movie_cast = 'Cast: ' + str(movie_descr[1]).replace('With', '').strip() if len(movie_descr) > 1 else ''
    movie_story = 'Story: ' + str(movie_descr[2]).strip() + '.' if len(movie_descr) > 2 else ''
    rating = s_data.find("span", class_="sc-bde20123-1 iZlgcd").text if s_data.find("span", class_="sc-bde20123-1 iZlgcd") else ''
    movie_rating = 'Total Rating count: ' + str(rating) if rating else ''

    return movie_director, movie_cast, movie_story, movie_rating

def KNN_Movie_Recommender(test_point, k):
    # Create dummy target variable for the KNN Classifier
    target = [0 for item in movie_titles]
    # Instantiate object for the Classifier
    model = KNearestNeighbours(data, target, test_point, k=k)
    # Run the algorithm
    model.fit()
    # Print list of 10 recommendations < Change value of k for a different number >
    table = []
    for i in model.indices:
        # Returns back movie title and imdb link
        table.append([movie_titles[i][0], movie_titles[i][2], data[i][-1]])
    return table

def run():
    
    root = tk.Tk()
    root.title("Movie Recommender System")
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Create a frame inside the canvas
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    img1 = Image.open('bg2.jpg')
    img1 = img1.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.BILINEAR)
    img1_tk = ImageTk.PhotoImage(img1)
    label = tk.Label(root, image=img1_tk)
    label.place(x=0, y=0, relheight=1, relwidth=1)
    img2 = Image.open('bg2.png')
    img2 = img2.resize((100, 100), Image.Resampling.BILINEAR)
    img2_tk = ImageTk.PhotoImage(img2)

    # Create a label with the logo image
    logo = tk.Label(root, image=img2_tk)
    logo.place(x=10, y=10)

    

    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']
    movies = [title[0] for title in movie_titles]
    category = ['--Select--', 'Movie based', 'Genre based']

    cat_op = tk.StringVar(root)
    cat_op.set('--Select--')

    tk.Label(root, text="Select Recommendation Type:", fg="white", bg="black", font=("Calibri", 15)).pack()
    tk.OptionMenu(root, cat_op, *category).pack()

    def on_select():
        if cat_op.get() == '--Select--':
            tk.messagebox.showwarning('Warning', 'Please select Recommendation Type!!')
        elif cat_op.get() == 'Movie based':
            select_movie = tk.StringVar(root)
            select_movie.set('--Select--')

            tk.Label(root, text="Select movie: (Recommendation will be based on this selection)").pack()
            tk.OptionMenu(root, select_movie, *movies).pack()

            def on_select_movie():
                if select_movie.get() == '--Select--':
                    tk.messagebox.showwarning('Warning', 'Please select Movie!!')
                else:
                    no_of_reco = tk.IntVar(root)
                    no_of_reco.set(5)

                    tk.Label(root, text="Number of movies you want Recommended:").pack()
                    scrollbar_frame = tk.Frame(root)
                    scrollbar = create_scrollbar(scrollbar_frame)
                    container = tk.Canvas(scrollbar_frame, yscrollcommand=scrollbar.set, bg="white")
                    scrollbar.configure(command=container.yview)

                    container.pack(side="left", fill="both", expand=True)
                    scrollbar_frame.pack(side="left", fill="both", expand=True)

                    tk.Scale(root, from_=5, to=20, orient='horizontal',fg="white", bg="red",  variable=no_of_reco).pack()

                    def on_submit():
                        if select_movie.get() == '--Select--':
                            tk.messagebox.showwarning('Warning', 'Please select Movie!!')
                        else:
                            genres = data[movies.index(select_movie.get())]
                            test_points = genres
                            table = KNN_Movie_Recommender(test_points, no_of_reco.get() + 1)
                            table.pop(0)
                            c = 0
                            tk.Label(root, text="Some of the movies from our Recommendation, have a look below").pack()
                            for movie, link, ratings in table:
                                c += 1
                                director, cast, story, total_rat = get_movie_info(link)
                                tk.Label(root, text=f"({c})[ {movie}]({link})").pack()
                                tk.Label(root, text=director).pack()
                                tk.Label(root, text=cast).pack()
                                tk.Label(root, text=story).pack()
                                tk.Label(root, text=total_rat).pack()
                                tk.Label(root, text='IMDB Rating: ' + str(ratings) + '⭐').pack()

                    tk.Button(root, text="Submit", fg="white", bg="red", command=on_submit).pack()

            tk.Button(root, text="Fetch Movie Poster", command=on_select_movie).pack()

        elif cat_op.get() == 'Genre based':
            sel_gen = tk.StringVar(root)
            sel_gen.set('')

            tk.Label(root, text="Select Genres:", bg="black", fg="white").pack()
            #for genre in genres:
                #tk.Checkbutton(root, text=genre, variable=sel_gen, onvalue=genre, offvalue='').pack()

            #dec = tk.StringVar(root)
            #dec.set('No')
            sel_gen = tk.StringVar(root)
            sel_gen.set('')

            #tk.Label(root, text="Select Genres:", fg="white", bg="red").pack()
            genre_dropdown = ttk.Combobox(root, textvariable=sel_gen, state="readonly", values=genres)
            genre_dropdown.pack()

            dec = tk.StringVar(root)
            dec.set('No')

            tk.Label(root, text="Want to Fetch Movie Poster?", fg="white", bg="black").pack()
            tk.Radiobutton(root, text="Yes", fg="white", bg="red",variable=dec, value='Yes').pack()
            tk.Radiobutton(root, text="No", fg="white", bg="red", variable=dec, value='No').pack()

            def on_submit():
                if sel_gen.get() == '':
                    tk.messagebox.showwarning('Warning', 'Please select Genres!!')
                else:
                    no_of_reco = tk.IntVar(root)
                    no_of_reco.set(5)

                    tk.Label(root, text="Number of movies you want Recommended:", fg="white", bg="red").pack()
                    tk.Scale(root, from_=5, to=20, fg="white", bg="red", orient='horizontal', variable=no_of_reco).pack()

                    def on_submit():
                        if sel_gen.get() == '':
                            tk.messagebox.showwarning('Warning', 'Please select Genres!!')
                        else:
                            test_point = [1 if genre in sel_gen.get().split(',') else 0 for genre in genres]
                            imdb_score = tk.IntVar(root)
                            imdb_score.set(8)

                            tk.Label(root, text="Choose IMDb score:", fg="white", bg="red").pack()
                            tk.Scale(root, from_=1, to=10, fg="white", bg="red", orient='horizontal', variable=imdb_score).pack()

                            table = KNN_Movie_Recommender(test_point, no_of_reco.get())
                            c = 0
                            tk.Label(root, text="Some of the movies from our Recommendation,have a look below").pack()
                            for movie, link, ratings in table:
                                c += 1
                                if dec.get() == 'Yes':
                                    image = movie_poster_fetcher(link)
                                    tk_image = ImageTk.PhotoImage(image)
                                    tk.Label(root, image=tk_image).pack()
                                director, cast, story, total_rat = get_movie_info(link)
                                tk.Label(root, text=f"({c})[ {movie}]({link})").pack()
                                tk.Label(root, text=director).pack()
                                tk.Label(root, text=cast).pack()
                                tk.Label(root, text=story).pack()
                                tk.Label(root, text=total_rat).pack()
                                tk.Label(root, text='IMDB Rating: ' + str(ratings) + '⭐').pack()

                    tk.Button(root, text="Submit", command=on_submit, fg="white", bg="red").pack()

            tk.Button(root, text="Fetch Movie Poster", fg="white", bg="red", command=on_submit).pack()

    tk.Button(root, text="Submit",fg="white", bg="red", command=on_select).pack()

    root.mainloop()

run()