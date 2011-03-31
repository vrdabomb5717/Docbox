import java.util.ArrayList;

//****************************************************************
// Battleboard.java
// This class represents a naval vessel such as a submarine or aircraft carrier.
// Written by Jervis Muindi.
// February 13, 2010.
//*****************************************************************

/**
 * This class represents the battleground for the game Battleship.
 */
public class Battleboard {

	/**
	 * Creates a battleboard object with the specified positions and orientation of the battleships.
	 * @param location location of the battleships
	 * @param orientation orientation of the battleships
	 * @param size the size of the ships.
	 */
	public Battleboard(String[] location, int[] orientation, int[] size){
		grid = new String[10][10];
		initialiseGrid();
		
		vessels = new ArrayList<Vessel>();
		for(int i = 0; i < location.length; i++){
			vessels.add(new Vessel(location[i],orientation[i],size[i])); // add a vessel object to the array list
		}
		
		shipLocations = getCoordinates();
		
	}
	
	private void initialiseGrid(){ //set all the points in the grid to be a space; otherwise grid will have null references
		for(int i = 0; i < 10; i++){
			for(int j = 0; j < 10; j++){
				grid[i][j] = " ";
			}
		}
	}
	
	/**
	 * This method checks if the coordinates of the ships chosen are valid legal positions.
	 * @return true if there are no problems and false when either a duplicate or an out of range coordinate is detected.
	 */
	public boolean coordinateCheck(){ 
		boolean outofrange = borderCheck();
		boolean duplicate = duplicateCheck();
		boolean pass = true;
		if (outofrange || duplicate){ // check if coordinates are duplicated or out of the board
			pass = false;
		}
		
		return pass;	
	}
	
	
	/**
	 * This method returns a string array containing the locations of the ships that have been setup on board. 
	 * @return a string array containing the locations of the ships that have been setup on board.
	 */
	public String[] getShipLocation(){
		return shipLocations;
	}
	
	private boolean borderCheck(){// Check if any of the points go outside of the 10 X 10 board.
		boolean isOutofrange = false;
		String[] coordinates = shipLocations;
		for(int i = 0; i < coordinates.length; i++){
			int length = (coordinates[i]).length(); 
			if(length > 3){ // ensure that coordinate is inside board by making sure it's length is exactly 3, e.g. "1,1".
				isOutofrange = true;
			}
		}
		return isOutofrange; 
	}
	
	
	private boolean duplicateCheck(){ // Check for duplicates in the points
		boolean duplicate = false;
		String[] coordinates = shipLocations;
		for(int i = 0; i < coordinates.length; i++){
			for(int j = i + 1; j < coordinates.length; j++){
				if(coordinates[i].equals(coordinates[j])){
					duplicate = true;
				}
			}
		}
		
		return duplicate;
	}
	
	
	/**
	 * Updates the grid array associated with the battleboard with an X for a Hit and O for a Miss using the specified location.
	 * @param x the x-coordinate of the location to be added to grid
	 * @param y the y-coordinate of the location to be added to grid
	 * @param s the nature of the update; either a "Hit" or a "Miss"
	 *  
	 */
	public void updateBoard(int x, int y, String s){
		if(s.equalsIgnoreCase("Hit")){
			grid[x][y] = "X";
		}
		else if(s.equalsIgnoreCase("Miss")){
			grid[x][y] = "O";
		}
	}
	
	/**
	 * Prints out the grid associated with this battleboard
	 */
	public void printBoard(){
		int[] column = {0,1,2,3,4,5,6,7,8,9};
		System.out.print(" ");
		for(int j = 0; j < 10; j++){
			System.out.print(" | ");
			System.out.print(column[j]);
		}
		System.out.println("\n"+"-----------------------------------------");
		for(int i = 0; i < 10; i++){
			System.out.print(i);
			for(int j = 0; j < 10; j++){
				System.out.print(" | ");
				System.out.print(grid[i][j]);
			}
			System.out.println("\n"+"-----------------------------------------");
		}
	}
	
	private String[] getCoordinates(){
		String[] coordinates= new String [17];
		int l = 0; // location index
		String[] temp;
		for(int i = 0; i < 5; i++){ // run 5 times
			temp =((vessels.get(i)).getCoordinates()); // get coordinates of current ship.
			for(int j = 0; j < temp.length; j++){
				if(l > 16){ 
					break; // then the string array is now full
				}
				else{
					coordinates[l] = temp[j];
				}
				l++; // update the location index counter
			}
		}
		
		
		return coordinates;
	}
		
		
	private ArrayList<Vessel> vessels;
	private String[][] grid;
	private String[] shipLocations;
}
