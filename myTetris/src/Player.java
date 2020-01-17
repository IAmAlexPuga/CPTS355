/* Play class that keeps track of current score and cleared blocks*/
public class Player {
	private int Score;
	private int ClearedBlocks;
	
	public Player() {
		this.Score = 0;
		this.ClearedBlocks = 0;
	}
	
	 // adds the sum to current score
	public void AddScore(int sum) {
		this.Score += sum;
	}
	
	// adds the sum to the current amount of blocks cleared
	public void AddBlocks(int sum) {
		this.ClearedBlocks += sum;
	}
	
	// returns the current score
	public int GetScore() {
		return this.Score;
	}
	
	// returns the current amount of blocks cleared
	public int GetBlocksCleared() {
		return this.ClearedBlocks;
	}
	
	// resets the current player stats
	public void ClearStats() {
		this.Score = 0;
		this.ClearedBlocks = 0;
	}

}
