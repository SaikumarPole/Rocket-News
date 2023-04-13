from django.urls import path
from . import apis, views

app_name= "news"

urlpatterns = [
    # path('api/user/update', apis..as_view(), name='update_user_api'),
    path('api/news/create/', apis.CreateNewsArticle.as_view(), name='create_news_article_api'),
    path('api/news/update/', apis.UpdateNewsArticle.as_view(), name='update_news_article_api'),
    path('api/news/remove/', apis.RemoveNewsArticle.as_view(), name='remove_news_article_api'),
    path('api/news/get_details/', apis.GetNewsArticleDetails.as_view(), name='get_news_article_details_api'),

    path('', views.NewsDashboard.as_view(), name='news_dashboard'),
    path('news_article/edit/<int:article_id>', views.EditNewsArticle.as_view(),name='edit_news_article'),
    path('news_article/create/', views.CreateNewsArticle.as_view(),name='create_news_article'),
    path('news_article/view/<int:article_id>', views.ViewNewsArticle.as_view(),name='view_news_article'),


]