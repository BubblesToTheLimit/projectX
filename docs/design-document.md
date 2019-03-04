## Description

A tool which can display spendings per category.

It can visualize the savings for the current month.

## Ideas for names
* FinanzViz
* FinanceViz
* Fynance
* Pynance

## Features
* parse a csv file from the sparkasse bank
* bookings can be analyzed based on defined tags
* bookings which can't be tagged will be tagged manually
    * update the tagconfig
* visualize the bookings with plotly
    * for a time interval (default: monthly)
    * per tag
* bookings can be edited after parsing
    * for example if the rent for february is withdrawn late (in march) 
    it should still show up in february

## Nice-to-have features
* A visual tagconfig builder (user-friendlyness)
* Run it as a web application inside a container
    * Either local...
    * ...or as a Server-Client application

## Possible tags
* Grundausgaben
    * Miete
    * Strom+Wasser
    * Handy
    * Internet
* Entertainment /Abos
    * Netflix
    * Amazon
    * Spotify
* Freizeit
    * Github
    * Kino
* Einkommen
* Essen