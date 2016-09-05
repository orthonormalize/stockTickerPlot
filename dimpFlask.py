from flask import Flask,render_template,request,redirect
from bokeh.plotting import figure
from bokeh.embed import components
import pandas as pd
import datetime
import calendar
import quandl
quandl.ApiConfig.api_key = 'u89rDBsvk1atKhVUzhLM'


def ticker2DF(ticker):
    # input: string that should correspond to a ticker symbol
    # output: pd DF with closing price data from the most recent month
		# output is an empty DF if the input string is not a valid ticker symbol
    today = datetime.datetime.date(datetime.datetime.now())
    if (today.month==1):
        (oldYear,oldMonth) = (today.year-1,12)
    else:
        (oldYear,oldMonth) = (today.year,today.month-1)
    oldDay = min([today.day,calendar.monthrange(oldYear,oldMonth)[1]])
    strStartDate = str(datetime.date(oldYear,oldMonth,oldDay))
    strEndDate = str(today)
    try:
        data = quandl.get("WIKI/" + ticker,start_date=strStartDate,end_date=strEndDate)
    except:
        data = pd.DataFrame({'Close':[]})
    closePrice = data['Close']
    return closePrice


app_rek = Flask(__name__)
app_rek.vars={}

@app_rek.route('/index.html',methods=['GET','POST'])
def route1():
	if request.method == 'GET':
		return render_template('htmlTemplate.html',myBokehScript='',myBokehDiv='Welcome to my stock ticker app. Enter a symbol above.')
	else:
		# request was a POST:
		app_rek.vars['ticker'] = request.form['tickerInput']
		closePriceData = ticker2DF(app_rek.vars['ticker'])
		p = figure(width=700, height=500, x_axis_type="datetime")
		p.line(closePriceData.index,closePriceData, color='red', alpha=0.5, line_width=4)
		p.xaxis.axis_label = "Date"
		p.yaxis.axis_label = "Closing Price (USD)"
		p.xaxis.axis_label_text_font_size = '18pt'
		p.yaxis.axis_label_text_font_size = '18pt'
		p.xaxis.major_label_text_font = '14pt'
		p.yaxis.major_label_text_font = '14pt'
		script,div = components(p)
		return render_template('htmlTemplate.html',myBokehScript=script,myBokehDiv=div)


if __name__ == '__main__':
    app_rek.run(debug=False,host='0.0.0.0')
