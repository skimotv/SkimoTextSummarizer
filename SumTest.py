import torch
from transformers import AutoTokenizer, AutoModelWithLMHead

# Use a model from https://huggingface.co/models?filter=summarization&sort=modified
models = ["sshleifer/distilbart-cnn-12-3", "sshleifer/distilbart-cnn-12-6",
          "sshleifer/distilbart-cnn-6-6", "sshleifer/distilbart-xsum-1-1",
          "sshleifer/distilbart-xsum-12-1", "sshleifer/distilbart-xsum-12-3",
          "sshleifer/distilbart-xsum-12-6", "sshleifer/distilbart-xsum-6-6",
          "sshleifer/distilbart-xsum-9-6", "google/pegasus-billsum"
          ]


tokenizer = AutoTokenizer.from_pretrained(models[9])
model = AutoModelWithLMHead.from_pretrained(models[9])

text = "Four overnight camps in Maine successfully identified and isolated three Covid-19 positive people with no symptoms, preventing transmission to more than 1,000 other campers and staff this summer, says a new report published by the Centers for Disease Control and Prevention.For many kids, summer camp looked and felt a little different this year. There were daily temperatures checks, more time spent outside and plenty of face masks. Dr. Laura Blaisdell of the Maine Medical Center Research Institute and colleagues said the extra effort paid off.They detailed where these camps went right in a report examining 642 children and 380 staff members who attended the four camps in Maine for well over a month between June and August.  Camp attendees traveled from across the United States and six international locations: Bermuda, Canada, Mexico, South Africa, Spain and the United Kingdom. They quarantined for up to 14 days before arriving at camp and three of the sites asked campers to submit Covid-19 test results before attending. This was an important step in preventing introduction of the virus in a setting with many young adults who could be asymptomatic or presymptomatic, Blaisdell and colleagues wrote in the CDC's weekly report.Camp attendees were separated into groups when they first arrived and had to wear face coverings when interacting with people outside of their groups. The camps kept surfaces clean and groups physically distant. They staggered bathroom use and dining times. They also screened campers daily for fever and coronavirus symptoms. Most attendees were tested again for Covid-19 a few days after arriving at camp. That's when a symptomless camper and two staff members tested positive, according to the report. They were rapidly isolated until they recovered, and their contacts were quarantined for 14 days.  (CNN)Four overnight camps in Maine successfully identified and isolated three Covid-19 positive people with no symptoms, preventing transmission to more than 1,000 other campers and staff this summer, says a new report published by the Centers for Disease Control and Prevention.For many kids, summer camp looked and felt a little different this year. There were daily temperatures checks, more time spent outside and plenty of face masks. Dr. Laura Blaisdell of the Maine Medical Center Research Institute and colleagues said the extra effort paid off.They detailed where these camps went right in a report examining 642 children and 380 staff members who attended the four camps in Maine for well over a month between June and August.A Georgia sleepaway camp&#39;s coronavirus outbreak is a warning for what could happen when schools reopen, CDC saysA Georgia sleepaway camp's coronavirus outbreak is a warning for what could happen when schools reopen, CDC saysCamp attendees traveled from across the United States and six international locations: Bermuda, Canada, Mexico, South Africa, Spain and the United Kingdom. They quarantined for up to 14 days before arriving at camp and three of the sites asked campers to submit Covid-19 test results before attending.Content by CNN UnderscoredHow to sell your old tech before it loses its value.CNN Underscored partnered with Decluttr to create this content. When you make a purchase, CNN receives revenue.This was an important step in preventing introduction of the virus in a setting with many young adults who could be asymptomatic or presymptomatic, Blaisdell and colleagues wrote in the CDC's weekly report.Camp attendees were separated into groups when they first arrived and had to wear face coverings when interacting with people outside of their groups. The camps kept surfaces clean and groups physically distant. They staggered bathroom use and dining times. They also screened campers daily for fever and coronavirus symptoms.Covid-19 child cases in the US have increased by 21% since early August, new data showsCovid-19 child cases in the US have increased by 21% since early August, new data showsMost attendees were tested again for Covid-19 a few days after arriving at camp. That's when a symptomless camper and two staff members tested positive, according to the report. They were rapidly isolated until they recovered, and their contacts were quarantined for 14 days.None of the contacts tested positive for Covid-19, according to the CDC report.The report noted that it wasn't one particular precaution that helped prevent the spread of coronavirus in these camps, but rather a multilayered strategy that was carefully executed."

print(len(text))


def summarize(text):
  inputs = tokenizer.encode(text, add_special_tokens=False, return_tensors="pt")
  outputs = model.generate(inputs, max_length=250, do_sample=True, top_p=0.95, top_k=60)
  generated = tokenizer.decode(outputs[0])
  return generated

sum = summarize(text)
print(sum)
print(len(sum))
