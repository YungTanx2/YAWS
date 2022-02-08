

from ast import If


class Letter:

    def __init__(self, letterScore, theLetter):
        #instance variables vs class variables are... interesting
        self.hasBeenGuessed = False
        self.isInWord = False
        self.correctPosition = -1
        self.score = 0
        self.impossiblePositions = []
        self.score = letterScore
        self.theLetter = theLetter

    def getLetter(self):
        return self.theLetter
    
    def setHasBeenGuessed(self, isGuessed):
        self.hasBeenGuessed = isGuessed
    
    def getHasBeenGuessed(self):
        return self.hasBeenGuessed
    
    def setIsInWord(self, isInWord):
        self.isInWord = isInWord
    
    def getIsInWord(self):
        return self.isInWord

    def addToImpossiblePositionList(self, positionToAdd):
        self.impossiblePositions.append(positionToAdd)
    
    def getImpossiblePositions(self):
        return self.impossiblePositions

    def setCorrectPosition(self, correctPosition):
        self.correctPosition = correctPosition
    
    def getCorrectPosition(self):
        return self.correctPosition

class WordGuessTracker:
    WordSize = 5
    theLetters = {}
    impossibleLetters = []
    missplacedLetters = {}
    correctLetters = {}
    theWordsAndScore = {}
    bestGuess = ''

    #initialize with list of all letters
    def __init__(self, letterScoreDictionary, wordScoreDictionary):
        for letter in letterScoreDictionary:
            #create new letter object and toss into letters
            self.theLetters[letter] = Letter(letterScoreDictionary[letter], letter)
            self.theWordsAndScore = wordScoreDictionary
        self.bestGuess = max(self.theWordsAndScore, key=self.theWordsAndScore.get)

    #function to check if word is possible
    def WordIsPossible(self, theWord):
        return False

    def UpdateGuess(self, guessResult):
        #need to ensure that we're doing 5 letter guesses
        if(len(guessResult) != self.WordSize):
            return "you dun f*cked up"
        
        #for each letter in result, update stuff
        for currentLetterIndex in range(0, self.WordSize):
            letterObject = self.theLetters[self.bestGuess[currentLetterIndex]]
            #regardless, current letter has been guessed
            letterObject.setHasBeenGuessed(True)
            #need to update the letter based on current guess
            match guessResult[currentLetterIndex]:
                case 'X':
                    #set that letter isn't in the word
                    letterObject.setIsInWord(False)
                    self.impossibleLetters.append(letterObject.getLetter())
                case 'Y':
                    #the letter is in the word (I feel like I dont need to do this...)
                    letterObject.setIsInWord(True)
                    #need to set current index as impossible
                    #####it's adding every impossible position to ever letter?
                    letterObject.addToImpossiblePositionList(currentLetterIndex)
                    self.missplacedLetters[letterObject.getLetter()] = letterObject
                case 'G':
                    #the Letter is in the word
                    letterObject.setIsInWord(True)
                    #the letter is in the correct position
                    letterObject.setCorrectPosition(currentLetterIndex)
                    #remove the letter from misplacedLetters
                    if(letterObject.getLetter() in self.missplacedLetters):
                        self.missplacedLetters.pop(letterObject.getLetter())
                    #add item to correct letter index
                    self.correctLetters[letterObject.getLetter()] = currentLetterIndex
                case _:
                    return "wtf did you do"
        #ok, now delete all guesses that are no longer possible
        #ok, for each word in the letter
        #well, cuz iterators, create new instance
        tempTheWordsAndScore = self.theWordsAndScore.copy()

        for wordToCheck in self.theWordsAndScore:
            if(wordToCheck == "wince"):
                1+1
            #tracking whether something should be popped, reset per loop
            popit = False
            #remove if it DOESN'T have the correct letter in place
            for correctLetter in self.correctLetters:
                letterInCorrectPosition = wordToCheck[self.correctLetters[correctLetter]]
                if(letterInCorrectPosition != correctLetter):
                    popit = True

            #does it contain an impossible letter?
            for impossibleLetter in self.impossibleLetters:
                if(impossibleLetter in wordToCheck):
                    popit = True
            
            #is there a letter in the wrong position and if it doesn't contain a missplaced letter
            for misplacedLetter in self.missplacedLetters.values():
                if((misplacedLetter.getLetter() not in wordToCheck)):
                    popit = True
                else:
                    #check if it has a letter, but in an impossible position
                    for position in misplacedLetter.getImpossiblePositions():
                        #check if the letter in the position exists
                        if(wordToCheck[position] == misplacedLetter.getLetter()):
                            #####OMFG OFF BY ONE ERRORS
                            popit = True
            if(popit):
                tempTheWordsAndScore.pop(wordToCheck)
        #set the word list to the altered word list
        self.theWordsAndScore = tempTheWordsAndScore
        #update the best guess
        self.bestGuess = max(self.theWordsAndScore, key=self.theWordsAndScore.get)

    def GetCurrentBestGuess(self):
        return self.bestGuess


###===========Start actual main method=======================###
#load word list
allZeWords = [line.rstrip() for line in open('5letterwords.txt')]

#apparently need to remove new line characters

howmanywords = len(allZeWords)
#calculate "score" of each letter by counting occurrence
#map of each letter, and uptick the score?
allthewordsinaline = ''.join(allZeWords).lower()

letterscore = {}
for letter in allthewordsinaline:
    if letter in letterscore:
        letterscore[letter] += 1
    else:
        letterscore[letter] = 1

#instead initialize wordguess object
wordscoredict = {}

for word in allZeWords:
    #calculate score
    score = 0
    temp = letterscore.copy()
    for letter in word:
        score += temp[letter]
        #this is the first guess, so setting score to 0
        temp[letter] = 0
    #add to map
    wordscoredict[word] = score


#initialize word guess tracker
wordguesstrackingobjectsuper = WordGuessTracker(letterscore, wordscoredict)

#determine best first letter word
	#just… pop the top?
thebestword = wordguesstrackingobjectsuper.GetCurrentBestGuess()
theguesss = ""
while (theguesss != "GGGGG"): 
    print(thebestword)
    print("sooo how'd I do?")
    theguesss = input("gimme result please: ").upper()

    
    wordguesstrackingobjectsuper.UpdateGuess(theguesss)
    thebestword = wordguesstrackingobjectsuper.GetCurrentBestGuess()
#recieve input from user
	#Something like XYXGGY

#transform guess to GuestResult Object

#Update WordGuess
	#remove letters that were blank
	#update IsInWord, isCorrectPosition and impossible positions
	
#Filter WordList based on updated WordGuess
	#foreach word
		#if banned letter, remove
			#need to track these?
		#if doesn't have correct lettes

#Pop the top word, and repeat