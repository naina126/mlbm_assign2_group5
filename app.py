import gradio as gr
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from urllib.parse import urlparse
import io
import numpy as np

def extract_article_title(url):
    """Extracts the article title from a Wikipedia URL."""
    parsed_url = urlparse(url)
    if parsed_url.hostname and parsed_url.hostname.endswith('wikipedia.org') and parsed_url.path.startswith('/wiki/'):
        return parsed_url.path.split('/wiki/')[-1]
    return None

def get_page_views(wiki_url, start_date_str, end_date_str, user_agent="MyWikipediaPageViewApp/1.0 (your_email@example.com)"):
    """Fetches Wikipedia page view data."""
    article_title = extract_article_title(wiki_url)

    if not article_title:
        return None

    api_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{project}/{access}/{agent}/{article}/daily/{start_date}/{end_date}"
    project = "en.wikipedia"
    access = "all-access"
    agent = "user"

    url = api_url.format(
        project=project,
        access=access,
        agent=agent,
        article=article_title,
        start_date=start_date_str,
        end_date=end_date_str
    )

    headers = {"User-Agent": user_agent}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if 'items' not in data:
            return None

        page_views = [{"Date": datetime.strptime(item['timestamp'][:8], '%Y%m%d').strftime('%Y-%m-%d'), "Views": item['views']} for item in data['items']]
        df = pd.DataFrame(page_views)
        df['Date'] = pd.to_datetime(df['Date'])
        return df

    except requests.exceptions.RequestException as e:
        return None
    except KeyError:
        return None
    except ValueError:
        return None

def plot_page_views(wiki_url1, wiki_url2, start_date, end_date):
    """Plots Wikipedia page views and returns the plot as an image."""
    wiki_urls = [wiki_url1, wiki_url2]

    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y%m%d')

    user_agent = "MyWikipediaPageViewApp/1.0 (your_email@example.com)"

    plt.figure(figsize=(12, 6))
    plot_made = False

    for wiki_url in wiki_urls:
        df = get_page_views(wiki_url, start_date, end_date, user_agent)
        if df is not None:
            article_title = extract_article_title(wiki_url).replace('_', ' ')

            # Highlight Spikes and Dips
            mean = df['Views'].mean()
            std = df['Views'].std()
            spikes = df[df['Views'] > mean + 2 * std]
            dips = df[df['Views'] < mean - 2 * std]

            plt.plot(df['Date'], df['Views'], label=article_title)
            plt.scatter(spikes['Date'], spikes['Views'], color='red', label=f'{article_title} Spikes')
            plt.scatter(dips['Date'], dips['Views'], color='blue', label=f'{article_title} Dips')

            plot_made = True

    if plot_made:
        plt.xlabel('Date')
        plt.ylabel('Page Views (Log Scale)')
        plt.title('Wikipedia Page Views Comparison')
        plt.legend()
        plt.grid(True)
        plt.yscale('log')

        return plt.gcf()
    else:
        plt.close()
        return None

iface = gr.Interface(
    fn=plot_page_views,
    inputs=[
        gr.Textbox(lines=1, placeholder="Enter first Wikipedia URL"),
        gr.Textbox(lines=1, placeholder="Enter second Wikipedia URL"),
        gr.Textbox(lines=1, placeholder="YYYYMMDD (leave blank for 30 days ago)"),
        gr.Textbox(lines=1, placeholder="YYYYMMDD (leave blank for today)")
    ],
    outputs=gr.Plot(),
    title="Wikipedia Page View Comparison",
    description="Enter two Wikipedia URLs and a date range to compare page views."
)

iface.launch()
