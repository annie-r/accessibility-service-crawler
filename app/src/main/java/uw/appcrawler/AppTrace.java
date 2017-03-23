package uw.appcrawler;

import java.util.ArrayList;

/**
 * Created by annieross on 3/22/17.
 */

public class AppTrace {
    private ArrayList<TraceStep> trace;
    private String name;

    public class TraceStep{
        private String type;
        private float x_coord;
        private float y_coord;
        private float wait;

    }
}
