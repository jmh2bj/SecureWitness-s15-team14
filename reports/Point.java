
public class Point implements Comparable{
	public float x, y;
	public String label;
	public double dist;
	public Point(float x, float y, String label) {
		this.x = x;
		this.y = y;
		this.label = label;
		dist = Double.MAX_VALUE;
	}
	
	@Override
	public String toString(){
		return label+" "+x+" "+ y + " " + dist;
	}

	public int compareTo(Object o) {
		// TODO Auto-generated method stub
		if(o instanceof Point) {
			Point p = (Point)o;
			if(dist - p.dist > 0)
				return 1;
			else if(dist - p.dist < 0)
				return -1;
		}
		return 0;
	}
	
	
}
