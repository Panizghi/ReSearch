# CS Big Cows List
List of people with great achievements in Computer Science.

## Docker Setup
Build docker image and run the container:
```
chmod u+x docker_run.sh
./docker_run.sh
```
To stop the docker container:
```
exit
```

## ACM awards WordCloud
The second part of this repository includes how to create a wordcloud regarding the ACM turing and fellow winners based on which category of computer science field they did that won the award. The category field was classified based on the award citation from the ACM website. The code utilized ChatGpt to generate the top CS fields which was contributed by the winners and perform the classification for each of the winners to the CS fields. Finally, we present the result as a word cloud which can be found in `gpt-classification/word_cloud`.

The code to generate this wordcloud can be run as follows:
```
pip install -r requirements.txt

```

To run the research crawler 
 cd ResearchCrawler
```
scrapy crawl acm_spider
```
  
