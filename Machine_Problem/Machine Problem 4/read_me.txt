	Araullo, John Art Marie G.							                                     
 	BSCS-NS-3A                                                                               
 	CS321L-M - Artificial Intelligence                                                                                      
 	Machine Problem #4                                                            	         
 	Six Men's Morris Game: The game can be played User vs. AI or User vs. User.              
 	Algorithm: Minimax with Alpha-Beta Pruning; Cutting Off Search                           
 	Please run the program on vscode terminal or pycharm.                                    
											                                                 
	CONSOLE-BASED SIX MEN'S MORRIS GAME						                                 
											                                                 
	GAMEPLAY									                                             
	1. Players take turns placing their pieces on the board, starting with Player 1.         
	A piece can be placed on any empty position on the board. The goal is to form            
	mills and prevent the opponent from doing the same.                                      
											                                                 
	2. After all pieces are placed, players take turns moving their pieces. A piece          
	can be moved to an adjacent empty position. If a move forms a mill, the player can       
	remove one of the opponent's pieces.                                                     
											                                                 
	3.  The game ends when a player has only two pieces left or is unable to make a move.    
	The player with more pieces on the board wins.                                           
											                                                 
	GAME SETUP									                                             
	Step 1: 									                                             
	Please choose Player 1:                                                                  
	1. Human Player                                                                          
	2. Computer Player                                                                       
        										                                             
	Step 2:                  							                                     
	Please choose Player 2:        							                                 
	1. Human Player   								                                         
	2. Computer Player                    						                             
											                                                 
	BOARD DISPLAY AND INPUT INSTRUCTIONS						                             
	. --------- . --------- .    a --------- b --------- c				                     
	|           |           |    |           |           |         			                 
	|    . ---- . ---- .    |    |    d ---- e ---- f    |				                     
	|   |               |   |    |   |               |   |				                     
	. - .               . - .    g - h               i - j 				                     
	|   |               |   |    |   |               |   |			  	                     
	|    . ---- . ---- .    |    |    k ---- l ---- m    |				                     
	|           |           |    |           |           |				                     
	. --------- . --------- .    n --------- o --------- p				                     
											                                                 
	PUT: Enter a lowercase letter representing the position where you want 		             
	to place your piece.								                                     
											                                                 
	MOVE: Enter two lowercase letters separated by a space, 			                     
	representing the starting and ending positions of the move.  			                 
											                                                 
	REMOVE: Enter a lowercase letter representing the position of the 		                 
	opponent's piece you want to remove.						                             
