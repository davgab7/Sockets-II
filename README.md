# Sockets-II

## Implementation Idea

I used Python multithreading to achieve the desired results for the program. To achieve a maximum of 3 clients connected at the same time, I keep track of the number of threades created, if the cpaacity exceeds 3 then a new client will not be able to connect until one of the previous clinets dissconnects.The Server will not crash but will display a thread overload message and send it to the client as well. It will ulimtaley refuse connection to the client. 

I named all the functions and variable appropriately so it should be very easy to follow the implementation logic

My backdoor is indexed from 1, so 0 will cause an error please don't do that. the prompt accpets y/n or a number. There is no bound checking as directed per the pdf. If a word is not specified, I pick one at random using the random module.

The maxium word length supported is 9. Words cannot exceed the charechter count of 9, that will result in undefined behaviour. 

The incorrect guesses is limited to 6

## Work Performed

All of the work was performed solely by myself

## Testing Results

Please find testing results outputs for the client and the server in client.txt and server.txt respectively. The test was performed using the backdoor to ge the word "heart" each time. The dictonary used was the default word file.
