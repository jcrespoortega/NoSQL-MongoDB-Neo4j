# Design 

In order to speed up the queries, we need to use some strategies and make an intelligence design. We split our data in two collections:

- Authors: 

  + Author's name. 
  + Publications array
  + Number of author's publications
  + Age
  
- Publications:

 + @key 
 + @mdate 
 + Author   
 + Type 
 + Year

To obtain an improvement in performance at some queries, we precalculate some tags. This strategy outpreform the same design without 
precalculous.
