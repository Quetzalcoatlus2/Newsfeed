import unittest
from unittest.mock import patch
import tkinter as tk
from PIL import ImageTk
from io import BytesIO
import requests

from Newsapi import display_articles_gui

class TestNewsAPI(unittest.TestCase):

    def setUp(self):
        self.articles = [
            {
                'title': 'Article 1',
                'source': {'name': 'Source 1'},
                'author': 'Author 1',
                'description': 'Description 1',
                'publishedAt': '2022-01-01',
                'url': 'https://www.example.com/article1',
                'urlToImage': 'https://www.example.com/image1.jpg'
            },
            {
                'title': 'Article 2',
                'source': {'name': 'Source 2'},
                'author': 'Author 2',
                'description': 'Description 2',
                'publishedAt': '2022-01-02',
                'url': 'https://www.example.com/article2',
                'urlToImage': 'https://www.example.com/image2.jpg'
            }
        ]
        self.error = 'Network error'
        self.status = 'Error'
        self.code = 500
        self.message = 'Internal Server Error'

    def test_display_articles_gui_with_articles(self):
        with patch('tkinter.Tk') as mock_tk:
            with patch('tkinter.Label') as mock_label:
                with patch('tkinter.Frame') as mock_frame:
                    with patch('tkinter.Canvas') as mock_canvas:
                        with patch('tkinter.Scrollbar') as mock_scrollbar:
                            with patch('tkinter.Label') as mock_title_label:
                                with patch('tkinter.Label') as mock_source_label:
                                    with patch('tkinter.Label') as mock_author_label:
                                        with patch('tkinter.Label') as mock_description_label:
                                            with patch('tkinter.Label') as mock_publishedAt_label:
                                                with patch('tkinter.Label') as mock_article_url_label:
                                                    with patch('tkinter.Label') as mock_url_label:
                                                        with patch('tkinter.Label') as mock_image_link_label:
                                                            with patch('tkinter.Label') as mock_urlToImage_label:
                                                                with patch('requests.get') as mock_requests_get:
                                                                    with patch('PIL.Image.open') as mock_image_open:
                                                                        with patch('PIL.Image.Image.resize') as mock_image_resize:
                                                                            with patch('PIL.ImageTk.PhotoImage') as mock_photo_image:
                                                                                with patch('tkinter.Label') as mock_img_label:
                                                                                    display_articles_gui(self.articles, None, None, None, None)
                                                                                    
                                                                                    # Assert that the necessary tkinter methods are called
                                                                                    mock_tk.assert_called_once()
                                                                                    mock_tk.return_value.title.assert_called_once_with("Articole")
                                                                                    mock_tk.return_value.grid_rowconfigure.assert_called_once_with(0, weight=1)
                                                                                    mock_tk.return_value.grid_columnconfigure.assert_called_once_with(0, weight=1)
                                                                                    mock_tk.return_value.mainloop.assert_called_once()
                                                                                    
                                                                                    mock_canvas.assert_called_once_with(mock_tk.return_value)
                                                                                    mock_canvas.return_value.configure.assert_called_once_with(yscrollcommand=mock_scrollbar.return_value.set)
                                                                                    mock_canvas.return_value.grid.assert_called_once_with(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
                                                                                    mock_canvas.return_value.create_window.assert_called_once_with((0, 0), window=mock_frame.return_value, anchor='nw')
                                                                                    mock_canvas.return_value.bind_all.assert_called_once_with("<MouseWheel>", mock_tk.return_value.on_mousewheel)
                                                                                    
                                                                                    mock_scrollbar.assert_called_once_with(mock_tk.return_value, orient='vertical', command=mock_canvas.return_value.yview)
                                                                                    mock_scrollbar.return_value.grid.assert_called_once_with(row=0, column=1, sticky=(tk.N, tk.S))
                                                                                    
                                                                                    mock_frame.assert_called_once_with(mock_canvas.return_value)
                                                                                    
                                                                                    # Assert that the necessary tkinter.Label methods are called
                                                                                    mock_title_label.assert_called_with(mock_frame.return_value, text="#1 Article 1", font=("Verdana", 10))
                                                                                    mock_title_label.return_value.grid.assert_called_with(row=0, sticky=(tk.W))
                                                                                    
                                                                                    mock_source_label.assert_called_with(mock_frame.return_value, text="Sursă: Source 1", font=("Arial", 12))
                                                                                    mock_source_label.return_value.grid.assert_called_with(row=1, sticky=(tk.W))
                                                                                    
                                                                                    mock_author_label.assert_called_with(mock_frame.return_value, text="Autori: Author 1", font=("Arial", 12))
                                                                                    mock_author_label.return_value.grid.assert_called_with(row=2, sticky=(tk.W))
                                                                                    
                                                                                    mock_description_label.assert_called_with(mock_frame.return_value, text="Scurtă descriere: Description 1", font=("Arial", 12))
                                                                                    mock_description_label.return_value.grid.assert_called_with(row=3, sticky=(tk.W))
                                                                                    
                                                                                    mock_publishedAt_label.assert_called_with(mock_frame.return_value, text="Publicat la: 2022-01-01", font=("Arial", 12))
                                                                                    mock_publishedAt_label.return_value.grid.assert_called_with(row=4, sticky=(tk.W))
                                                                                    
                                                                                    mock_article_url_label.assert_called_with(mock_frame.return_value, text="Link articol:  ", font=("Arial", 12))
                                                                                    mock_article_url_label.return_value.grid.assert_called_with(row=5, sticky=(tk.W))
                                                                                    
                                                                                    mock_url_label.assert_called_with(mock_frame.return_value, text="https://www.example.com/article1", font=("Arial", 12), fg="blue", cursor="hand2")
                                                                                    mock_url_label.return_value.grid.assert_called_with(row=5, padx=100, sticky=(tk.W))
                                                                                    mock_url_label.return_value.bind.assert_called_with("<Button-1>", lambda event, url="https://www.example.com/article1": mock_tk.return_value.open_url(event, url))
                                                                                    
                                                                                    mock_image_link_label.assert_called_with(mock_frame.return_value, text="Link imagine: ", font=("Arial", 12))
                                                                                    mock_image_link_label.return_value.grid.assert_called_with(row=6, sticky=(tk.W))
                                                                                    
                                                                                    mock_urlToImage_label.assert_called_with(mock_frame.return_value, text="https://www.example.com/image1.jpg", font=("Arial", 12), fg="blue", cursor="hand2")
                                                                                    mock_urlToImage_label.return_value.grid.assert_called_with(row=6, padx=100, sticky=(tk.W))
                                                                                    mock_urlToImage_label.return_value.bind.assert_called_with("<Button-1>", lambda event, url="https://www.example.com/image1.jpg": mock_tk.return_value.open_url(event, url))
                                                                                    
                                                                                    mock_requests_get.assert_called_with("https://www.example.com/image1.jpg")
                                                                                    mock_requests_get.return_value.content.assert_called_once()
                                                                                    
                                                                                    mock_image_open.assert_called_with(BytesIO(mock_requests_get.return_value.content))
                                                                                    mock_image_resize.assert_called_with((1500, 500))
                                                                                    mock_photo_image.assert_called_with(mock_image_resize.return_value)
                                                                                    
                                                                                    mock_img_label.assert_called_with(mock_frame.return_value, image=mock_photo_image.return_value)
                                                                                    mock_img_label.return_value.image.assert_called_with(mock_photo_image.return_value)
                                                                                    mock_img_label.return_value.grid.assert_called_with(row=7, sticky=(tk.W))
                                                                                    
    def test_display_articles_gui_with_error(self):
        with patch('tkinter.Tk') as mock_tk:
            with patch('tkinter.Label') as mock_label:
                display_articles_gui(None, self.error, self.status, self.code, self.message)
                
                # Assert that the necessary tkinter methods are called
                mock_tk.assert_called_once()
                mock_tk.return_value.title.assert_called_once_with("Articole")
                mock_tk.return_value.grid_rowconfigure.assert_called_once_with(0, weight=1)
                mock_tk.return_value.grid_columnconfigure.assert_called_once_with(0, weight=1)
                mock_tk.return_value.mainloop.assert_called_once()
                
                # Assert that the necessary tkinter.Label methods are called
                mock_label.assert_called_with(mock_tk.return_value, text="Network error: Network error", font=("Arial", 12))
                mock_label.return_value.grid.assert_called_with(row=1, column=0, sticky=(tk.W))
                
    def test_display_articles_gui_with_no_articles(self):
        with patch('tkinter.Tk') as mock_tk:
            with patch('tkinter.Label') as mock_label:
                display_articles_gui([], None, None, None, None)
                
                # Assert that the necessary tkinter methods are called
                mock_tk.assert_called_once()
                mock_tk.return_value.title.assert_called_once_with("Articole")
                mock_tk.return_value.grid_rowconfigure.assert_called_once_with(0, weight=1)
                mock_tk.return_value.grid_columnconfigure.assert_called_once_with(0, weight=1)
                mock_tk.return_value.mainloop.assert_called_once()
                
                # Assert that the necessary tkinter.Label methods are called
                mock_label.assert_called_with(mock_tk.return_value, text="Nu s-au găsit articole. Încercați din nou.", font=("Arial", 12))
                mock_label.return_value.grid.assert_called_with(row=0, column=0, sticky=(tk.W))

if __name__ == '__main__':
    unittest.main()