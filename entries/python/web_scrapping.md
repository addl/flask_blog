## poster
![Object Usage over time in JVMs](https://drive.google.com/uc?id=1W-bfYG9sTPW-FtFf-ERjldQLj5ekbJ2n)

## Introduction
Web scraping is a powerful technique used to extract information from websites. In this article, we will explore a Python code snippet that demonstrates how to scrape universities' data from a web page using the lxml library and XPath. 

## What is LXML
Lxml stands for XML and HTML, lxml is the most feature-rich and easy-to-use library for processing XML and HTML in the Python language.
The lxml XML toolkit is a Pythonic binding for the C libraries libxml2 and libxslt. It is unique in that it combines the speed and XML feature completeness of these libraries with the simplicity of a native Python API.

## What is XPath
XPath stands for XML Path Language. It uses a non-XML syntax to provide a flexible way of addressing (pointing to) different parts of an XML document. It can also be used to test addressed nodes within a document to determine whether they match a pattern or not.
XPath is mainly used in XSLT, but can also be used as a much more powerful way of navigating through the DOM of any XML-like language document using XPathExpression, such as HTML and SVG.

## Installing libraries
We need to install the required libraries. Run the following command to install them all at once:
```commandline
pip install requests lxml
```
This command will install the `requests`, and `lxml` libraries.

## The scrapping process

The scraping process, in general, involves the following steps:

1. To study the HTML page we want to extract information from. 
2. Making HTTP requests using `requests` library to get the HTML. 
3. Parsing the HTML content using `lxml` module. 
4. Extracting specific data using `XPath` expressions. 

Let's go one step at a time.

## Studying the website
For this entry, I will scrap data from this [website](https://webometrics.info/en/world). On this website we can find all universities in the world. The information is shown in a table with the following format:
```html
<table class="sticky-enabled tableheader-processed sticky-table">
   <thead>
      <tr>
         <th class="active"><a href="/en/world?sort=desc&amp;order=ranking" title="sort by ranking" class="active">ranking</a></th>
         <th><a href="/en/world?sort=asc&amp;order=University" title="sort by University" class="active">University</a></th>
         <th>$nbsp;</th>
         <th>Country</th>
      </tr>
   </thead>
   <tbody>
      <tr class="odd">
         <td>
            <center>1</center>
         </td>
         <td><a href="https://ror.org/03vek6s52" target="_blank">Harvard University</a></td>
         <td></td>
         <td>
            <center><img alt="bandera" src="https://webometrics.info/sites/default/files/logos/us.png"></center>
         </td>
      </tr>
      <tr>More 'tr' elements ....</tr>
   </tbody>
</table>
```

> To see the structure of any page in the browser, perform right-click on any place on the page a select inspect element to see the document structure.

For simplicity, I extracted the relevant HTML snippet. By analyzing the HTML we can infer the following:

1. We have for every university a `tr` element inside the body of the table. 
2. For every row(`tr` element) in the 2nd column of the table, we have an `a` element with the university's name, in this example is `Harvard University`. 
3. For every row(`tr` element) in the 4th column of the table, we have a `img` element, inside a `center` element, with the country where this university is located. 

> To get the country we have to read the `src` attribute of the `img` element and get the country code, in this case is `us`.

## Making requests
After the analysis we are ready to perform the requests:
```python
response = requests.get("https://webometrics.info/en/world")
byte_string = response.content
```
This code sends an HTTP GET request to the specified URL using the `requests` library. The **get()** function is used to send a GET request to the specified URL. The URL in this case is "https://webometrics.info/en/world", which is the target web page from which we want to retrieve data.
By accessing the attribute `content` of the HTTP response we access to the raw response content in bytes, we store it in the `byte_string` variable. We will use this raw response to get the DOM of the HTML page.

## Parsing HTML
```python
source_code = html.fromstring(byte_string)
```
The above code uses the **fromstring()** function from the `html` module of the `lxml` library to parse the HTML content. It converts the byte string into an HTML document object, represented by the `source_code` variable. This HTML document object allows us to access and manipulate the elements in the DOM.

## Extracting the data using XPath expressions
At this point we have a full HTML page inside the `source_code` variable, so we are ready to traverse the DOM using XPATH. From our analysis we have to iterate through all the rows in the table. We could fetch all rows using the following XPATH expression:

`"//*[@id='block-system-main']/div/table/tbody/tr"`

Now here is the big tip, I AM NOT A XPATH GURU, instead I used Chrome browser to assist me in this matter, by inspecting the HTML, I can get the XPATH expression by doing the following:

![Spring STS Dashboard](https://drive.google.com/uc?id=1mTd8FioidaOROTFFvfmjgJJU7BYDb49Z)

This will give me the following expression `//*[@id="block-system-main"]/div/table[2]`, then I modified it a bit to get `//*[@id='block-system-main']/div/table/tbody/tr`, that basically fetch all rows in the body of all tables found within the HTML document.

Now lets fetch all rows as follows:
```python
rows = source_code.xpath("//*[@id='block-system-main']/div/table/tbody/tr")
```
Now we will process each row by accessing its columns(`td` elements) and getting the data for university's names and country code:
```python
for uni_elem in rows:
    university = uni_elem.xpath(".//td[2]/a")[0].text
    country_path = uni_elem.xpath(".//td[4]/center/img")[0].attrib['src']
    country_code = os.path.basename(country_path)[:2]
    if country_code in universities_by_country:
        the_list = universities_by_country.get(country_code)
        the_list.append(university)
        universities_by_country[country_code] = the_list
    else:
        universities_by_country[country_code] = [university]
    print(universities_by_country)
```
Here is the full explanation of the above code:

1. The code iterates over each university element in the rows list. 
2. The university name is obtained by selecting the anchor element `a` within the second column `td[2]`. 
3. The country code is extracted from the `src` attribute of the `img` element within the 4th table cell `td[4]/center/img`. 
4. The extracted university name and country code are stored in variables university and country_code, respectively. 
5. The data is stored in a dictionary in the format: 
```json
{"us": ["Harvard University", "...."]}
```
Finally, the dictionary is printed in the output console.

## Full script code
Here is how the full script looks like:
```python
import os.path
import requests
from lxml import html


def get_universities_data() -> {}:
    universities_by_country = {}
    response = requests.get("https://webometrics.info/en/world")
    byte_string = response.content
    source_code = html.fromstring(byte_string)
    rows = source_code.xpath("//*[@id='block-system-main']/div/table/tbody/tr")
    for uni_elem in rows:
        university = uni_elem.xpath(".//td[2]/a")[0].text
        country_path = uni_elem.xpath(".//td[4]/center/img")[0].attrib['src']
        country_code = os.path.basename(country_path)[:2]
        if country_code in universities_by_country:
            the_list = universities_by_country.get(country_code)
            the_list.append(university)
            universities_by_country[country_code] = the_list
        else:
            universities_by_country[country_code] = [university]
    print(universities_by_country)


if __name__ == "__main__":
    get_universities_data()
```

## Executing the scrapper
If you have the code saved in a file named `universities_scraper.py`, you can run it using the following command:
```commandline
python universities_scraper.py
```
After executing the script, the result will be similar to this output:
```json
{
   "us":[
      "Harvard University",
      "Stanford University",
   ],
   "uk":[
      "University of Oxford",
   ],
   "ca":[
      "University of Toronto",
   ],
   ...
}
```
Congratulations! You have extracted information using scrapping and Python.

## A challenge for you
The website only lists a few universities, in order to get all universities, you have to navigate through the site using the page parameter as follows:

`https://webometrics.info/en/world?page=1`

So you should make N request to the site with the specific page number to get the remaining universities. Practice the techniques learned in this post, and customize the script to retrieve the full list of universities. Happy code!

## Conclusion
In this article, we demonstrated how we can get advantage of web scraping using the LXML library and XPath to extract information from different websites. 
The code extracted universities' data from a web page and organized it by country. After this article, you can now start your own web scraping journey and gather valuable data for research, business intelligence, and various other applications.

## References

[LXML Website](https://lxml.de/)