# Wikipedia Page View Comparison App

This application allows you to compare the page views of two Wikipedia articles over a specified date range. It uses the Wikimedia REST API to fetch page view data and visualizes the results using a Gradio interface.

## Getting Started

### Prerequisites

* A GitHub account.
* Google Colab (or a Python environment with the necessary packages).

### Installation

1.  **Clone the Repository:**
    * If you're using Google Colab, run the following in a code cell:

        ```bash
        !git clone [https://github.com/naina126/mlbm_assign2_group5.git](https://github.com/naina126/mlbm_assign2_group5.git)
        ```

    * Replace `https://github.com/naina126/mlbm_assign2_group5.git` with the actual URL of your repository.

2.  **Install Dependencies:**
    * Navigate to the cloned directory:

        ```bash
        %cd mlbm_assign2_group5
        ```

    * Install the required Python packages:

        ```bash
        !pip install -r requirements.txt
        ```

### Usage

1.  **Run the Application:**
    * In your Colab notebook, execute the `app.py` script:

        ```python
        !python app.py
        ```

2.  **Access the Gradio Interface:**
    * Gradio will generate a public URL. Click on the URL to open the interface in your browser.

3.  **Enter Wikipedia URLs:**
    * In the Gradio interface, enter the Wikipedia URLs you want to compare in the provided text boxes.
    * Example URLs:
        * `https://en.wikipedia.org/wiki/Python_(programming_language)`
        * `https://en.wikipedia.org/wiki/Java_(programming_language)`

4.  **Enter Date Range (Optional):**
    * You can specify a date range in `YYYYMMDD` format.
    * If you leave the date range blank, the application will use the last 30 days.

5.  **View the Plot:**
    * The application will display a plot comparing the page views of the two articles over the specified date range.
    * The plot will highlight spikes and dips in page views.

## File Structure
mlbm_assign2_group5/
├── app.py           # The main application code.
└── requirements.txt # The list of Python dependencies.
└── README.md        # This file.

## Dependencies

* `gradio`
* `requests`
* `pandas`
* `matplotlib`
* `numpy`

## Notes

* Ensure you have a stable internet connection to fetch data from the Wikimedia API.
* The application uses a log scale for the Y-axis (page views) to better visualize large variations in data.
* The application highlights spikes and dips that are more than 2 standard deviations away from the mean.
* Replace `your_email@example.com` in the user agent with your actual email address.

## Author

* naina126
