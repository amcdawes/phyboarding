# Physics Dashboards
## Open tools for physics data display and analysis

In-class hands-on data collection and display facilitated by open-source hardware and software tools. Presented at AAPT Winter Meeting 2020.

Slides from that talk are available in the PDF file AAPTWM2020.pdf.

Hardware used for this work is the [Adafruit Circuit Playground Express](https://www.adafruit.com/product/3333).

### Install python:
Installation is easiest using the [Anaconda Distribution](https://www.anaconda.com/distribution/). Once that distribution is installed, use conda to create a virtual environment that includes the necessary requirements:

### Create a virtual environment:
`conda create -f environment.yml`

### Activate your new venv:
`conda activate phyboard`

To roll your own installation, clone this repository and install the following required packages:
 - python 3 (It's 2020 folks, time to use 3)
 - bokeh
 - plotly
 - dash
 - pyserial
