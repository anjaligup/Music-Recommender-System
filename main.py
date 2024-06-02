################################################
# GLOBAL VARIABLES                             #
################################################
file = "musicrecplus.txt" 
artists = []
publicUsers = {}

################################################
# MAIN BODY FUNCTIONS                          #
################################################

# greeting function ############################

def greeting():
  #everyone
  #the main greeting the user gets when starting the program. Sets name variable and sets artists to previous artists if name is returning user 
  
  try: 
    #try statement creates music reccomender file if it doesnt exist 
    open(file, 'r')
  except FileNotFoundError as error:
      open('musicrecplus.txt','x')
    
  ignorePriv()
  
  global name
  name = input('Welcome to the music recommender, please enter your name. Put a $ at the end of your name for private mode): \n')
  if not(findNameInFile(name)):
    enterPref()
  else:
    setPreviousPref()
    menu()

def setPreviousPref():
  #if a name exists in the file, it sets artists as their previous preferences
  wholeFile = open(file, "r") 
  for line in wholeFile:
    [userName, listOfArtists]= line.strip().split(":")
    if userName == name:
      global artists
      artists = listOfArtists.strip().split(",")
  
def ignorePriv():
  #creates a dictionary of users (keys) and artists that are not in private mode 
  wholeFile = open(file, "r") 
  for line in wholeFile:
    [userName, listOfArtists]= line.strip().split(":")
    listOfArtists = listOfArtists.split(",")
    listOfArtists.sort()

    if not(userName[-1] == "$"):
      publicUsers[userName] = listOfArtists
  wholeFile.close()
  
def findNameInFile(name):
  #everyone
  #returns whether a name is in the file already
  with open(file, 'r') as wholeFile:
    for line in wholeFile:
      [username, prefs] = line.strip().split(":")
      if name == username:
        return True
    wholeFile.close()
    return False

# menu ##########################################

def menu():
  # everyone
  #prints options for user 
  option = input("Enter a letter to choose an option: \ne - Enter preferences \nr - Get recommendations \np - Show most popular artists \nh - How popular is the most popular \nm - Which user has the most likes \nq - Save and quit\n")
  if option == 'q':
    saveAndQuit()
  elif option == "e":
    enterPref()
  elif option == 'r':
    getRecs(name, artists, publicUsers)
  elif option == 'p':
    showPopArtists()
  elif option == 'h':
    mostPop()
  elif option == 'm':
    mostLikes()
  else: # option != 'e' or 'r' or 'p' or 'h' or 'm':
    print('Please choose one of the following options')
    return menu()
  

# enter preferences ##################################
    
def enterPref():
  # everyone 
  # takes in user input as artist preferences 
  artist = input("Enter an artist that you like (Enter to finish): \n")
  while artist != "":
    artists.append(artist)
    artist = input("Enter an artist that you like (Enter to finish): \n")
  standardize(artists)
  #if username exists, wipe their artists from 
  
  menu()

# standardize musicians #############################

def standardize(musicians):
  #standardizies artists (global) list, and sorts them in alphabetical order
  newList = []
  for i in range(len(musicians)):
      newList.append(musicians[i].strip().title())
  newList.sort()
  global artists 
  artists = newList

# get recommendations ###################################

def getRecs(name, artists, publicUsers):
  #returns the recommended artist of the current users. combined getRec and findBestUser
  if publicUsers == {} or artists == []:
    print("No recommendations available at this time")
    
  else:
    #count matches
    current_matches = 0
    most_matches = 0 
    current_key = ""
    key_of_most = ""

    for artistList in publicUsers:
      if not(artistList == name):
        current_key = artistList
        current_matches = numMatches(publicUsers[artistList], artists)
        if current_matches > most_matches and len(publicUsers[artistList]) > current_matches:
          most_matches = current_matches
          key_of_most = current_key
  
    #in the case nothing matches; is this what we do?
    if most_matches == 0:
      print("No recommendations available at this time")
      
    
   #return recs
  
    else:
      newArtists = []
      
      for i in range(len(publicUsers[key_of_most])):
        if (publicUsers[key_of_most][i] not in artists):
          newArtists.append(publicUsers[key_of_most][i])
    
      for artist in newArtists:
          print(artist.strip())
  menu()

def numMatches(pubUse, art):
  # returns the number of matches between two lists (more consise version of textbook)
  matches = 0
  for artist in art:
    if artist in pubUse:
      matches += 1
  return matches

# most popular artists #######################

def showPopArtists():
  #prints the top 3 artists appeared in music file
  popArtistsHelper1()
  top = dict(popArtists1)
  for artist in popArtists1:
    if popArtists1[artist]<2:
      del top[artist]
  top3new1 = list(top.keys())    
  print(top3new)
  if len(top3new1) >0:
    print(top3new1[0])
    if len(top3new1)>1:
      print(top3new1[1])
      if len(top3new1)>2:   
        print(top3new1[2])
  menu()
  



popArtists1 = {}
def popArtistsHelper1():
  ignorePriv()
  '''makes a dictionary of artists and the amount of times they appear in the document in order of most to least popular (includes current user)'''
  global popArtists1
  global artists
  global name
  global usernames
  artistslist1 = artists
  usernames = []
  with open(file, "r") as wholeFile:
    for line in wholeFile:
      [username, prefs] = line.strip().split(":")
      if username in publicUsers:
        artists = prefs.strip().split(",")
        for artist in artists:
          if name != username:
            artistslist1 = artistslist1 + [artist]
    #print(artistslist)
    artistslist1.sort
    #print(artistslist)
    for artist in artistslist1:
      x = artistslist1.count(artist)
      if artist not in popArtists1:
        popArtists1[artist] = x
  popArtists1 = dict(sorted(popArtists1.items(),key = lambda x:x[1], reverse = True ))
  
  
# how popular most popular artist is ######

def mostPop():
  #returns the most popular artist's score
  global popArtists
  popArtistsHelper1()
  values = popArtists1.values()
  values = list(values)
  print(values[0])
  menu()

# which user likes the most artists #####

def mostLikes():
  # returns the user(s) who like the most artists 
  users_and_artists = []
  for user in publicUsers:
    userAndArtists = [user, len(publicUsers[user])] 
    users_and_artists.append(userAndArtists) 
  users_and_artists.append([name, len(artists)])

  users_and_artists = selectionSort(users_and_artists)

  returningList = [users_and_artists[0][0]]
  highestLikes = users_and_artists[0][1]
  users_and_artists = users_and_artists[1:]

  for listt in users_and_artists:
    if listt[1] == highestLikes:
      returningList.append(listt[0])
    else:
      break

  print(returningList[0])
  menu()

def selectionSort(users_and_artists):
  #sorts a list of users and artists by second element in the list representing the numbers of artists they like 
  length = len(users_and_artists)

  for i in range(length - 1):
      max_index = i

      for j in range(i + 1, length):
          if users_and_artists[j][1] > users_and_artists[max_index][1]:
              max_index = j

      users_and_artists[i], users_and_artists[max_index] = users_and_artists[max_index], users_and_artists[i]

  return users_and_artists
    
# save and quit #######################################

def saveAndQuit():
  global artists
  artists1 = format(artists)
  if findNameInFile(name)== False:
    #if name is not already in file, it adds it to the end 
    with open(file, 'a') as f:
      f.write('\n' + name + ': ' + artists1)
      f.close()
  else:
    #if name is in file, it replaces it
    wholeFile = []
    with open(file, 'r') as f:
      for line in f:
          [username, prefs] = line.strip().split(":")
          if username == name:
            #print(artists)
            prefs = artists
          else:
            prefs = prefs.strip().split(",")
          
          wholeFile.append([username,prefs])
    with open(file, 'w') as f2:
      whole = ""
      for pair in wholeFile:
        line = ""
        line += (pair[0] +":")
        for i in range(len(pair[1])):
          line += (pair[1][i])
          if not(i==len(pair[1])-1):
            line += (",")
        line += ("\n")
        whole += line
      f2.write(whole)

def format(list):
  #this function converts the list of artists to a string with the correct formatting
  string = str(sorted(list)) 
  string = string.replace("'",'')
  return string[1:-1].title()

######RUNNING PROGRAM##############
greeting()
