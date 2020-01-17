import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
//import java.io.Console; //Enable this if you would like to print on the console for debugging

import javax.swing.BorderFactory;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.Timer;

public class Board extends JPanel  implements ActionListener {
	/*define constants for customizing the game */
	public  final int BOARD_WIDTH = 10; //number of rows in the board
	public  final int BOARD_HEIGHT = 20; //number of columns
	public final int CELL_WIDTH = 30;
	public final int CELL_HEIGHT = 35;	
    public  final char SPACE = ' ';
    public  final String TARGET = "355";
    
    private final int DELAY = 400;
    private static final Color BLACK =  new Color(0,0,0);
    
    private Timer timer;  //We use the java.util.Timer to create a game cycle. The shapes move on a square by square basis (not pixel by pixel).
    private boolean isFallingFinished = false; //isFallingFinished is set to true when the fall of a piece is completed; it is set to false when the next piece starts to fall. 
    private boolean isStarted = false;  //isStarted is set to false when the board height reaches the limit and the next piece can't be moved (i.e., game is over). The program exist when isStarted becomes false. 
    private boolean isPaused = false;   //set to true when the game is paused; false otherwise.
    private JLabel statusbar; 
    private JLabel scorebar;  //The label displaying the game score
    private JLabel scoretext; 
    private Font textFont;
    private Piece curPiece;   //The current (falling) piece
    private char [][] board; //The board grid
    private int [][] boardChecker; // Helper board
    private Player playa; // Player stats

    
    public Board(Tetris parent) {

        initBoard(parent);
    }
    
    /*clear all cells on the board. A cell in the board is considered empty if the character at that cell is SPACE. Iniatially all cells are initialized with SPACE.*/
    private void clearBoard() {
        for (int i = 0; i < BOARD_HEIGHT; i++) {
        	for (int j = 0; j < BOARD_WIDTH; j++) {
        		board[j][i] = SPACE;
        	}
        }
        playa.ClearStats();
    }
    
    /*calculate the cell width and height in pixels*/
    private int squareWidth() { return (int) getSize().getWidth() / BOARD_WIDTH; }
    private int squareHeight() { return (int) getSize().getHeight() / BOARD_HEIGHT; }
    
    /*calculate the X coordinate of the left upper corner of j th cell on a row. (j is a 0-based index)*/  
    private int calcX(int j) {
    	return (j * squareWidth());
        
    }
    /*calculate the Y coordinate of the left upper corner of i th cell on a column. (i is a 0-based index)*/  
    private int calcY(int i) {
        Dimension size = getSize();
    	int boardTop = (int) size.getHeight() - BOARD_HEIGHT * squareHeight(); 
    	return (boardTop + i * squareHeight());
        
    }
    /*initialize the game board, create the first piece, and start the timer */
    private void initBoard(Tetris parent) {
        
       setFocusable(true);
       playa = new Player();
       curPiece = new Piece();
       //create the Timer. The board object is registered as the listener  for the timer. When the timer is fired, Board's action listener method will be called. 
       timer = new Timer(DELAY, this);
       timer.start(); 

   	   this.textFont = new Font("Helvatica", Font.BOLD, 22);
       statusbar = parent.getStatusBar(); //get the reference to the Tetris's status bar
       scorebar = parent.getScoreBar();   //get the reference to the Tetris's score bar
       scoretext = parent.getScoreText();   //get the reference to the Tetris's score bar
       
       scoretext.setFont(textFont);
       scorebar.setBorder(BorderFactory.createEtchedBorder(1));
       scorebar.setFont(textFont);
       statusbar.setFont(textFont);
       
       addKeyListener(new TAdapter());
       //create and clear the board
       board = new char [BOARD_WIDTH] [BOARD_HEIGHT];
       boardChecker = new int [BOARD_WIDTH][BOARD_HEIGHT]; 
       clearBoard();    
       
    }

    /* When Timer is fired, Board's override of actionPerformed will be called*/
    @Override
    public void actionPerformed(ActionEvent e) {
        /*if the falling of the current piece is completed, create a new piece*/
        if (isFallingFinished) {        
            isFallingFinished = false;
            createNewPiece();
        } else{ // else move the current piece one level down on the board.     
            oneLineDown();
        }
    }

/* Start the game. */  
    public void start()  {
        
        if (isPaused)
            return;

        isStarted = true;
        isFallingFinished = false;
        
        createNewPiece();
        timer.start();
        clearBoard();
    }
    /* Pause the game. */  
    private void pause()  {
        
        if (!isStarted)
            return;

        isPaused = !isPaused;
        
        if (isPaused) {
            
            timer.stop();
            statusbar.setText("PAUSED");
        } else {
            
            timer.start();
            statusbar.setText(" ");
        }
        
        repaint();
    }

    /* draw a square over the non-empty board cells (a cell is non-empty if its value is not SPACE). The color of the cell is determined based on the cell value. */
    private void drawSquare(Graphics g, int x, int y, char number)  {
        
        Color colors[] = { new Color(50, 150, 50), new Color(204, 102, 102), 
            new Color(102, 204, 102), new Color(102, 102, 204), 
            new Color(204, 204, 102), new Color(204, 102, 204), 
            new Color(0, 255, 0), new Color(0, 0, 255),
            new Color(102, 204, 204), new Color(218, 170, 0)
        };

        Color color = colors[Character.getNumericValue(number)];

        g.setColor(color);
        g.fillRect(x + 1, y + 1, squareWidth() - 2, squareHeight() - 2);
        g.setColor(BLACK);
        g.setFont(textFont);
        g.drawString(String.valueOf(number), x+(squareWidth()-(CELL_WIDTH/2)+1)/2, y+(squareHeight()+(CELL_HEIGHT/2))/2 );
             
        g.setColor(color.brighter());
        g.drawLine(x, y + squareHeight() - 1, x, y);
        g.drawLine(x, y, x + squareWidth() - 1, y);

        g.setColor(color.darker());
        g.drawLine(x + 1, y + squareHeight() - 1,
                         x + squareWidth() - 1, y + squareHeight() - 1);
        g.drawLine(x + squareWidth() - 1, y + squareHeight() - 1,
                         x + squareWidth() - 1, y + 1);

    }

    /*draw the squares for the non empty cells on the board (already dropped pieces and the current piece currently falling)*/
    private void doDrawing(Graphics g) {       
   	
    	/*draw the squares for already dropped pieces*/
        for (int i = 0; i < BOARD_HEIGHT; i++) {
            for (int j = 0; j < BOARD_WIDTH; j++) {
                if (board[j][i] != SPACE) {
                	drawSquare(g, calcX(j),calcY(i), board[j][i]);
                }
            }
        }
        /*draw the square for the currently dropping piece*/
        if (curPiece.getNumber() != SPACE) {                
                drawSquare(g, calcX(curPiece.getX()),calcY(curPiece.getY()), curPiece.getNumber());
            
        }        
    }

    /*Board's overwrite for paintComponent. This will be called every time "repaint() is called . */
    @Override
    public void paintComponent(Graphics g) { 

        super.paintComponent(g);
        doDrawing(g);
    }

    /*move the current piece all the way down on the board*/
    private void dropDown() {
        
        int newY = curPiece.getY();
        
        while (newY < BOARD_HEIGHT-1) {
            
            if (!tryMove(curPiece, 0 , 1))
                break;
            ++newY;
        }
        
        pieceDropped();
    }
   
    /*move the current piece one row down on the board*/
    private void oneLineDown()  {
        
        if (!tryMove(curPiece, 0, 1))
            pieceDropped();
    }


    /*checks if the fall of the current piece is completed. 
     * **TODO** If so, updates the board and the score.*/
    private void pieceDropped() {                
        updateBoard(curPiece); 

        if (!isFallingFinished)
            createNewPiece();
    }

    /*creates the new piece; if the board is full (i.e, can't move the current piece) stops the game. */  
    private void createNewPiece()  {
        
        curPiece.setRandomNumber();
        curPiece.setX(BOARD_WIDTH / 2 + 1);
        curPiece.setY(0);

        if (!tryMove(curPiece, 0, 0)) {
            
            curPiece.setNumber(SPACE);
            timer.stop();
            isStarted = false;
            statusbar.setText("GAME OVER");
        }
    }

    /*moves the current piece by newX,newY on the Board and repaints the Board*/
    private boolean tryMove(Piece newPiece, int newX, int newY) {
        int x = newPiece.getX() + newX;
        int y = newPiece.getY() + newY;
           
        if (x < 0 || x >= BOARD_WIDTH || y < 0 || y >= BOARD_HEIGHT)
        	return false;     
        
        if (board[x][y] != SPACE)
            return false;
       

        curPiece = newPiece;
        curPiece.setX(x);
        curPiece.setY(y);

        repaint();

        return true;
    }
    
    /*Updates the Board: 
     * clears all cell groups including 3 (or more) matching adjacent cells
     * clears all cell groups including the target characters 
     *     - can appear either horizontal(left to right or right to left )  or vertical (up to down or down to up)
     *     - the characters of the target string need to appear in the same order.*/
    public void updateBoard(Piece curPiece) {
        
    	board[curPiece.getX()][curPiece.getY()] = curPiece.getNumber();
    	
        /*Updates the Board:
         * checks to see if the the current piece placed groups 3 or more matching
         * adjacent cells. If it does it:  
         * -clears all cell groups including 3 (or more) matching adjacent cells
         * -clears all cell groups including the target characters.
         * if not then it resets the board checker */
    	if(clearPieceCheck(curPiece.getNumber(),curPiece.getX(),curPiece.getY()) > 2){
    		clearPiece(curPiece.getNumber(),curPiece.getX(), curPiece.getY());
    		boardChecker = new int [BOARD_WIDTH][BOARD_HEIGHT];
    		moveItemsDown();
    		repaint();
    	}else {
    		boardChecker = new int [BOARD_WIDTH][BOARD_HEIGHT];
    	}
    	/* checks to see if there exists a bonus after piece is inserted.
    	 * checks to see if there can be more pieces removed when items are moved down
    	 * moves all units down if any floating pieces exists*/
    	checkBonus();
    	checkMovedItems();
    	moveItemsDown();
    	// updates the score board with the players current score
    	scorebar.setText(String.valueOf(playa.GetScore()));
     }
    
    /* checks the moved pieces to make sure there is no new groups with 
     * 3 or more same adjacent pieces*/
    public void checkMovedItems() {
    	for(int x = 0; x < BOARD_WIDTH; x++){
    		for(int y = 0; y < BOARD_HEIGHT; y++){
    			
    			if(board[x][y] != SPACE)
    			{
    				if(clearPieceCheck(board[x][y],x,y) > 2)
    				{
    		    		// removes the group of pieces
    					clearPiece(board[x][y],x,y);
    					// adds the amount removed * 5
    		    		int count = count();
    		    		playa.AddBlocks(count);
    		    		playa.AddScore(count * 5);
    		    		// resets the board and moves everything down
    		    		boardChecker = new int [BOARD_WIDTH][BOARD_HEIGHT];
    		    		moveItemsDown();
    		    		repaint();
    				}else {
    					boardChecker = new int [BOARD_WIDTH][BOARD_HEIGHT];
    				}
    			}
    		}
    	}
    }
    
    /*Moves all items down if applicable*/
    public void moveItemsDown() {
    	char temp;
    	for(int x = 0; x < BOARD_WIDTH; x++){
    		for(int y = 0; y < BOARD_HEIGHT - 1; y++){
    			if (board[x][y] != SPACE && board[x][y+1] == SPACE){
    				temp = board[x][y];
    				board[x][y] = SPACE;
    				board[x][y+1] = temp;
    				if(y-2 > 0) {
    					y -=2;
					}
    			}
    		}
    	}
    	
    }
    
    /* counts the number of elements in boardChecker to 
     * help calculate the score*/
    public int count()
    {
    	int count = 0;
    	for(int x = 0; x < BOARD_WIDTH; x++){
    		for(int y = 0; y < BOARD_HEIGHT; y++){
    			if(boardChecker[x][y] == 1) {
    				count += 1;
    			}
    		}
    	}
    	return count;
    }
    
    /* checks for any bonuses in the board.  if any are found then add to the 
     * score*/
    public void checkBonus() {
    	int mult = 0;
    	for(int x = 0; x < BOARD_WIDTH - 2; x++){
    		for(int y = 0; y < BOARD_HEIGHT - 2; y++){
    			if(board[x][y] == '3' && board[x + 1][y] == '5' && board[x + 2][y] == '5')
    			{
    				board[x][y] = SPACE;
    				board[x+1][y] = SPACE;
    				board[x+2][y] = SPACE;
    				mult += 1;
    			}else if(board[x][y] == '3' && board[x][y+1] == '5' && board[x][y+2] == '5') {
    				board[x][y] = SPACE;
    				board[x][y+1] = SPACE;
    				board[x][y+2] = SPACE;
    				mult += 1;
    			}else if (board[x][y] == '5' && board[x + 1][y] == '5' && board[x + 2][y] == '3') {
    				board[x][y] = SPACE;
    				board[x+1][y] = SPACE;
    				board[x+2][y] = SPACE;
    				mult += 1;
    			}else if (board[x][y] == '5' && board[x][y+1] == '5' && board[x][y+2] == '3') {
    				board[x][y] = SPACE;
    				board[x][y+1] = SPACE;
    				board[x][y+2] = SPACE;
    				mult += 1;
    			}else if (board[x][y+1] == '3' && board[x + 1][y+1] == '5' && board[x + 2][y+1] == '5') {
    				board[x][y+1] = SPACE;
    				board[x+1][y+1] = SPACE;
    				board[x+2][y+1] = SPACE;
    				mult += 1;
    			}else if (board[x][y+2] == '3' && board[x + 1][y+2] == '5' && board[x + 2][y+2] == '5') {
    				board[x][y+2] = SPACE;
    				board[x+1][y+2] = SPACE;
    				board[x+2][y+2] = SPACE;
    				mult += 1;
    			}
    		}
    	}
    	// Adds the players bonus points here
    	mult *= 20;
    	playa.AddBlocks((mult / 20) * 3);
    	playa.AddScore(mult);
    }
    
    /* clears the grouping of same piece recursively */
    public void clearPiece(char curPiece, int x, int y)
    {
    	if (x > BOARD_WIDTH - 1 || y > BOARD_HEIGHT - 1 || x < 0 || y < 0 || boardChecker[x][y] != 1)
    	{
    		return;
    	}
    	if( boardChecker[x][y] == 1)
    	{
    		playa.AddScore(5);
        	playa.AddBlocks(1);
    		boardChecker[x][y] = 0;
    		board[x][y] = SPACE;
    		clearPiece(curPiece, x , y - 1);
    		clearPiece(curPiece, x -1 , y);
    		clearPiece(curPiece, x + 1, y);
    		clearPiece(curPiece, x, y + 1);
    	}
    }
    
    /* checks the new piece added to the board if it creates a grouping */
    public int clearPieceCheck(char curPiece, int x, int y)
    {
    	// makes sure its between the boards boundary
    	if (x > BOARD_WIDTH - 1 || y > BOARD_HEIGHT - 1 || x < 0 || y < 0 || boardChecker[x][y] == 1)
    	{
    		return 0;
    	}
    	if(board[x][y] == 0 || board[x][y] != (char)curPiece)
    	{
    		return 0;
    	}
    	if(board[x][y] == (char)curPiece)
    	{
    		// marks the board and looks all around the piece
    		boardChecker[x][y] = 1;
    		return 1 + clearPieceCheck(curPiece, x , y - 1) + 
    				clearPieceCheck(curPiece, x -1 , y) + 
    				clearPieceCheck(curPiece, x + 1, y) + 
    				clearPieceCheck(curPiece, x, y + 1);
    	}else {
    		return 0;
    	}
    }

  

    /* handles the key presses*/
    class TAdapter extends KeyAdapter {
        
         @Override
         public void keyPressed(KeyEvent e) {

             if (!isStarted || curPiece.getNumber() == SPACE) {  
                 return;
             }

             int keycode = e.getKeyCode();

             if (keycode == 'P') {
                 pause();
                 return;
             }

             if (isPaused)
                 return;

             switch (keycode) {
                 
             case KeyEvent.VK_LEFT:
                 tryMove(curPiece, - 1, 0);
                 break;
                 
             case KeyEvent.VK_RIGHT:
                 tryMove(curPiece,  1, 0);
                 break;
                 
             case KeyEvent.VK_DOWN:
            	 tryMove(curPiece, 0, 2);
                 break;
                 
             case KeyEvent.VK_UP:
                 tryMove(curPiece, 0, 0);
                 break;
                 
             case KeyEvent.VK_SPACE:
                 dropDown();
                 break;
                 
             case 'D':
                 oneLineDown();
                 break;
             }
         }
     }
}
