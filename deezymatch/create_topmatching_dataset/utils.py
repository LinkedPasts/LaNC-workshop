import argparse
import re
import os
import sys
import datetime
import pandas as pd
from pathlib import Path
from random import shuffle
import multiprocessing as mp
from geopy.distance import great_circle
from Levenshtein import distance as levDist
from IPython.display import display, clear_output
import random
import tqdm
from functools import partial
import mysql.connector
from mysql.connector import Error

# -----------------------------------------------------------
# CREATE A MINIMAL WIKIGAZETTEER
# -----------------------------------------------------------
def create_minimal_gaz(wikigaz_db, username_db, password_db, min_wikigaz):
    gazDB = ""
    cursorGaz = ""
    try:
        gazDB = mysql.connector.connect(
                host='localhost',
                database=wikigaz_db,
                user=username_db,
                password=password_db)
        if gazDB.is_connected():
            cursorGaz = gazDB.cursor(buffered=True)
    except Error as e:
        print("Error while connecting to MySQL", e)
        
    cursorGaz.execute("""SELECT altname, wiki_title, lat, lon, source FROM altname
                         JOIN location ON altname.main_id = location.id""")
    locs = cursorGaz.fetchall()
    wgdf = pd.DataFrame(locs, columns =['altname', 'pid', 'lat', 'lon', 'source'])
    
    # Close DB connection:
    if (gazDB.is_connected()):
        cursorGaz.close()
        gazDB.close()
    
    wgdf = wgdf[wgdf["source"].isin(['wikimain', 'geonamesmain', 'geonamesascii', 'geonamesalt', 'wikiredirect'])]
    wgdf = wgdf[wgdf["altname"].str.len() < 30]
    wgdf['lat'] = wgdf['lat'].astype(float)
    wgdf['lon'] = wgdf['lon'].astype(float)
    wgdf = wgdf[wgdf['lat'].notna()]
    wgdf = wgdf[wgdf['lon'].notna()]
    wgdf = wgdf.rename(columns={"altname": "name", "pid": "wikititle", "lat": "latitude", "lon": "longitude"})
    wgdf.to_pickle(min_wikigaz + ".pkl")
    
    return wgdf


# -----------------------------------------------------------
# FILTER LOCATIONS ACCORDING TO COORDINATE BOUNDING BOXES
# -----------------------------------------------------------

def filter_gaz_by_bbox(lat, lon, bboxes):
    for bbox in bboxes:
        if lat > bbox[1] and lat < bbox[3] and lon > bbox[0] and lon < bbox[2]:
            return True
    return False


# -----------------------------------------------------------
# CREATE A STRING MATCHING TRAINING DATASET
# -----------------------------------------------------------

def get_placename_and_unique_alt_names(place_dict):
    """given a place we retrieve altnames and location (we don't use location for the moment)"""
    
    placename = place_dict['placename']
    unique_alt_names = list(place_dict['altnames'])
    placeloc = (place_dict["lat"], place_dict["lon"])
    
    return placename, unique_alt_names, placeloc

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
def get_ngrams(placename, maxngrams,minngrams):
    
    ngrams = []
    for nlen in range(maxngrams,minngrams,-1):
        for ii in range(len(placename)-nlen+1):
            ngrams.append(placename[ii:(ii+nlen)])
    return ngrams


def get_final_wrong_cands_challenging(cand_ngrams,unique_alt_names,placename,placeloc,n_neg_cand_to_generate,place_id, altnames, kilometre_distance, wiki_ids):

    selected_wrong_cands = set()
    
    """
    for each ngram, we send a query to the DB
    at the moment i'm parallelizing at the placename step, but this could be also parallelized
    so searching different ngrams at the same time
    """
    # We take all altnames that:
    # * contain the a candidate ngram
    # * are not possible positive altnames of the toponym
    # * are not exact matches of the toponym
    # * their length difference with respect to the toponym is less than 5 characters
    for cand_ngram in cand_ngrams:
        collected_wrong_cands = {x for x in altnames.keys() if cand_ngram in x if place_id not in altnames[x] and x!= placename and x not in unique_alt_names and (abs(len(x) - len(placename)) <= 5)}
        for k in collected_wrong_cands:
            if k not in selected_wrong_cands:
                selected_wrong_cands.add(k)
    
    # we filter out alternate names that can correspond to locations within 50 km from
    # the main location
    mindistance = kilometre_distance
    filtered_by_distance = set()
    for x in selected_wrong_cands:
        within_distance = False
        for alt in altnames[x]:
            lat_alt = float(wiki_ids[alt]["lat"])
            lon_alt = float(wiki_ids[alt]["lon"])
            lat_main = float(wiki_ids[place_id]["lat"])
            lon_main = float(wiki_ids[place_id]["lon"])
            if great_circle((lat_alt, lon_alt), (lat_main,lon_main)).km < mindistance:
                within_distance = True
                break
        if within_distance == False:
            filtered_by_distance.add(x)
                
    selected_wrong_cands = filtered_by_distance
        
    if len(selected_wrong_cands)<1:
        return None
    
    # we rank them using LevDist so that we have on top the most similar wrong ones 
    rank_wrong_cands = [[placename,x,levDist(x,placename)] for x in selected_wrong_cands]
    
    # we sort them, from more similar to less (unlike in the trivial setting)
    rank_wrong_cands.sort(key=lambda x: x[2])
    
    # and we keep only the top n, depending on the number of positive candidates
    final_wrong_cands = rank_wrong_cands[:n_neg_cand_to_generate]
    
    return final_wrong_cands

def get_final_wrong_cands_trivial(unique_alt_names,placename,placeloc,n_neg_cand_to_generate,place_id, altnames):

    selected_wrong_cands = set()
    
    # We take 50 random altnames that:
    # * are not possible positive altnames of the toponym
    # * are not exact matches of the toponym
    # * their length difference with respect to the toponym is less than 5 characters
    collected_wrong_cands = {x for x in random.sample(altnames.keys(), 50)}
    for k in collected_wrong_cands:
        if place_id not in altnames[k] and k != placename and k not in unique_alt_names and (abs(len(k) - len(placename)) <= 5):
            if k not in selected_wrong_cands:
                selected_wrong_cands.add(k)
        
    if len(selected_wrong_cands)<1:
        return None
    
    # we rank them using LevDist so that we have on top the most similar wrong ones 
    rank_wrong_cands = [[placename,x,levDist(x,placename)] for x in selected_wrong_cands]
    
    # we sort them, from more dissimilar to less (unlike in the challenging setting):
    rank_wrong_cands.sort(key=lambda x: x[2], reverse=True)
    
    # and we keep only the top n, depending on the number of positive candidates
    final_wrong_cands = rank_wrong_cands[:n_neg_cand_to_generate]
    
    return final_wrong_cands

def normalized_lev(s1, s2):
    return 1 - int(levDist(s1, s2)) / float(max(1, len(s1), len(s2)))

def generate_cands(dt, place_id):

    wiki_ids = dt[0]
    altnames = dt[1]
    kilometre_distance = dt[2]

    place_dict = wiki_ids[place_id]

    placename, unique_alt_names, placeloc = \
            get_placename_and_unique_alt_names(place_dict)

    challenging_alt_names = [u for u in unique_alt_names if u != placename]
    challenging_alt_names = [u for u in challenging_alt_names if normalized_lev(u, placename) > 0.25]

    final_cands_chall = []
    final_cands_trivial = []
    final_cands = []

    """
    ### CHALLENGING PAIRS:
    """
    if len(challenging_alt_names)>0:
        
        # the number of neg candidates depend on the number of positive candidates
        n_neg_cand_to_generate = len(challenging_alt_names)
        
        """
        this has a huge impact on performance. it's the number of ngrams we will retrieve
        at the moment n is equal to length of the placename -1 to -3
        for Barcelona: ['Barcelon', 'arcelona', 'Barcelo', 'arcelon', 'rcelona']
        other cutoffs will give better results, but the number of queries will explode
        like this, with -3 and -5: ['Barcel','arcelo','rcelon','celona','Barce','arcel','rcelo','celon','elona']
        --- Update (4 Sep 2020)
        Using:         
        maxcutoff = len(placename)-1
        mincutoff = len(placename)-3
        
        will result in more challenging/interesting examples. (current setting) 
        
        The downside is that the number of found pairs will be 
        less than more generous cutoffs, e.g.:
        
        maxcutoff = len(placename)-1
        mincutoff = 1
        Take the example:
        s1 = "London" 
        cand_ngrams = get_ngrams(s1,len(s1)-1,1); print(cand_ngrams)
        OUTPUT:
        ['Londo', 'ondon', 'Lond', 'ondo', 'ndon', 'Lon', 'ond', 'ndo', 'don', 'Lo', 'on', 'nd', 'do', 'on']
        whereas:
        cand_ngrams = get_ngrams(s1,len(s1)-1,len(s1)-3); print(cand_ngrams) 
        OUTPUT:
        ['Londo', 'ondon', 'Lond', 'ondo', 'ndon']
        There are different ways to deal with these cases, e.g.:
        * We could pass the whole cand_ngrams and have a break in get_final_wrong_cands_challenging, i.e.
        stop searching for pairs when a specific number of candidates is reached
        * Pass cand_ngrams = cand_ngrams[:N] 
        """
        
        maxcutoff = len(placename)-1
        mincutoff = len(placename)-5

        cand_ngrams = get_ngrams(placename,maxcutoff,mincutoff)
        
        # now, having a set of ngams, we try to retrieve negative candidates
        # so candidates that are similar based on ngrams overlap, like Marcelona for Barcelona
        final_cands_chall = get_final_wrong_cands_challenging(cand_ngrams,challenging_alt_names,placename,placeloc,n_neg_cand_to_generate,place_id,altnames, kilometre_distance, wiki_ids)

        if final_cands_chall != None:
            # we keep only placename and wrongcand and add the label False
            final_cands_chall = [x[:2]+["False"] for x in final_cands_chall]
                
            # we double check and in case the number of neg is less than the pos
            # we take only a random selection of the positive
            
            n_final_wrong = len(final_cands_chall)

            shuffle(challenging_alt_names)
            
            # we add the positive as well with the label
            for i in range(n_final_wrong):
                alt_name_cand = [placename,challenging_alt_names[i],"True"]
                final_cands_chall.append(alt_name_cand)

    """
    ### TRIVIAL PAIRS: (if we indented twice: if there are challenging pairs, we also get trivial pairs,
    as it is now: for each toponym, get trivial pairs)
    """

    trivial_alt_names = [u for u in unique_alt_names if u.lower() == placename.lower()]

    # Randomly with probabily 1/20 we add a lower-cased toponym or upper-cased toponym as alternate name:
    random_add = random.choice(range(0,20))
    if random_add == 2:
        trivial_alt_names.append(placename.lower())
    if random_add == 3:
        trivial_alt_names.append(placename.upper())

    # the number of neg candidates depend on the number of positive candidates
    n_neg_cand_to_generate = len(trivial_alt_names)

    # we try to retrieve negative trivial pairs for as many positive pairs
    final_cands_trivial = get_final_wrong_cands_trivial(trivial_alt_names,placename,placeloc,n_neg_cand_to_generate,place_id,altnames)

    if final_cands_trivial != None:
        # we keep only placename and wrongcand and add the label False
        final_cands_trivial = [x[:2]+["False"] for x in final_cands_trivial]

        # we double check and in case the number of neg is less than the pos
        # we take only a random selection of the positive

        n_final_wrong = len(final_cands_trivial)

        shuffle(trivial_alt_names)

        # we add the positive as well with the label
        for i in range(n_final_wrong):
            alt_name_cand = [placename,trivial_alt_names[i],"True"]
            final_cands_trivial.append(alt_name_cand)
    
    # We join trivial and challenging pairs   
    if final_cands_trivial:
        final_cands += final_cands_trivial

    if final_cands_chall:
        final_cands += final_cands_chall
    
    if final_cands:
        return final_cands

    else:
        return None

def create_pairmatch_dataset(N, titles_per_chunk, wikigaz_df, kilometre_distance, output_name):

    out = open(output_name, "w")
    
    if not type(N) == int:
        N = mp.cpu_count()

    p = mp.Pool(processes = N)

    tot = 0
    start = datetime.datetime.now()

    wikigaz_df["name"] = wikigaz_df['name'].str.replace('(','')
    wikigaz_df["name"] = wikigaz_df['name'].str.replace(')','')
    wikigaz_df.to_csv("tmp_wikigaz.tsv", sep = "\t", 
                      columns = ["wikititle", "name", "latitude", "longitude", "source"], 
                      header=False, index=False)

    # we retrieve wiki_ids and altnames and we structure them in two dictionaries (wiki_title -> altnames and altname -> wiki_titles)
    wiki_variations = open("tmp_wikigaz.tsv", "r").read().strip().split("\n")
    wiki_variations = [x.split("\t") for x in wiki_variations]
    wiki_variations = [[x[0]]+[x[0].replace("_"," ").replace('"','')]+x[1:] for x in wiki_variations]

    wiki_ids = {x[0]:{"placename":x[1], "altnames":set(),"lat":"","lon":""} for x in wiki_variations}
    altnames = {x[2]:set() for x in wiki_variations}

    for x in wiki_variations:
        if len(wiki_ids[x[0]]["altnames"])==0:
            wiki_ids[x[0]]["lat"] = x[3]
            wiki_ids[x[0]]["lon"] = x[4]

        if x[2] not in wiki_ids[x[0]]["altnames"]:
            wiki_ids[x[0]]["altnames"].add(x[2])

        if x[0] not in altnames[x[2]]:
            altnames[x[2]].add(x[0])

    wiki_titles = [x for x in wiki_ids.keys()]

    shuffle(wiki_titles)

    # we organize it in chunks, each chunk has titles_per_chunk titles
    wiki_titles_splits = list(chunks(wiki_titles, titles_per_chunk))
    n_splits = len(wiki_titles_splits)
    
    # i have divided the list of wiki titles in small chunks 
    # so i can process a few at a times and identify how long it will take
    for split in tqdm.tqdm(wiki_titles_splits):
        
        func = partial(generate_cands, (wiki_ids, altnames, kilometre_distance))

        # we assign them to different processes
        res = p.map(func, split)

        # we exclude the Nones
        res = [x for x in res if x!= None]
        res = [y for x in res for y in x if len(y)>1]
        
        #write out the results
        for el in res:
            out.write('\t'.join(el)+"\n")
            tot += 1

    out.close()