package uw.appcrawler;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.GestureDescription;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Rect;
import android.os.Bundle;
import android.view.accessibility.AccessibilityEvent;
import android.graphics.Path;
import android.util.Log;
import net.sourceforge.yamlbeans.YamlReader;
import android.content.res.AssetManager;

import android.view.accessibility.AccessibilityNodeInfo;

import java.sql.Timestamp;
import java.text.SimpleDateFormat;

import java.io.InputStreamReader;
import java.util.Map;
import java.util.ArrayList;

/**
 * Created by annieross on 3/16/17.
 */

public class Crawler extends AccessibilityService {

    private static final SimpleDateFormat sdf = new SimpleDateFormat("yyyy.MM.dd.HH.mm.ss");
    private String app_name = "Test";
    private static final String TAG = "Crawler";
    private BroadcastReceiver receiver_crawl;
    private final float back_x = 330;
    private final float back_y = 2480;
    private class Scanner{
        public final float scan_x=725;
        public final float scan_y=670;
        public final long wait_millis = 10000;
        public final float share_x=1200;
        public final float share_y=180;
        public final float drive_x=1219;
        public final float drive_y=1709;
        public final float title_x=200;
        public final float title_y= 475;
        public final float save_x=1270;
        public final float save_y=2320;
    };
    private final Scanner scanner = new Scanner();



    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {

    }

    @Override
    public void onInterrupt(){

    }

    /* broadcast command
        adb shell am broadcast -a crawler.startCrawl --es traversalFile <fileName in app/assets/traversals> --es appName <app Name>
         */
    @Override
    public void onCreate() {
        super.onCreate();
        Log.i(TAG, "onCreate");


        final IntentFilter filter_crawl = new IntentFilter();
        filter_crawl.addAction("crawler.startCrawl");
        receiver_crawl = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                Log.i(TAG, "broadcast start crawl");
                String traversal_file = intent.getStringExtra("traversalFile");
                app_name = intent.getStringExtra("appName");
                if(app_name == null){
                    app_name = "Unknown";
                }
                startCrawl(traversal_file);
            }
        };
        this.registerReceiver(receiver_crawl, filter_crawl);

    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        this.unregisterReceiver(receiver_crawl);
    }

    /*
    Crawl Format:
    types:
        click: coord_x, coord_y
        text: content, coord_x, coord_y
        wait: duration
        scan
        screenshot

     */
    public void startCrawl(String traversalFile){
        Log.i(TAG, "startCrawl");

        try {
            AssetManager assetsManager = getAssets();
            String[] files = assetsManager.list("");
            for (int i=0; i<files.length; ++i){
                System.out.println(files[i]);
            }
            Log.i(TAG, "file: "+files[0]);
            Log.i(TAG, "travFile: "+traversalFile);

            YamlReader reader = new YamlReader(new InputStreamReader(assetsManager.open("Traversals/"+traversalFile)));
            while(true) {
                Map step = (Map) reader.read();
                if (step == null) break;
                ArrayList command = (ArrayList) step.get("commands");
                Log.i(TAG, "commands: " + command.toString());
                for(int i=0; i<command.size(); ++i){
                    Map details = (Map) command.get(i);
                    String type = (String) details.get("type");
                    Log.i(TAG, "type: " + type);
                    switch (type) {
                        case "click":
                            click(Float.valueOf((String) details.get("x_coord")), Float.valueOf((String) details.get("y_coord")));
                            break;
                        case "text":
                            String content = (String) details.get("content");
                            int x_coord = Integer.valueOf((String) details.get("x_coord"));
                            int y_coord = Integer.valueOf((String) details.get("y_coord"));
                            enterText(content, x_coord, y_coord);
                            break;
                        case "wait":
                            Long duration = Long.valueOf((String) details.get("duration"));
                            Log.i(TAG, "wait: " + duration );
                            appWait(duration);
                            break;
                        case "scan":
                            scan();
                            break;
                        case "screenshot":
                            break;
                        default:
                            Log.e(TAG, "unknown command type: "+type);
                            break;
                    }
                }

            }
        } catch (Exception e){
            Log.e(TAG, e.toString());
        }

    }

    private void enterText(String content, int x_coord, int y_coord){
        Log.i(TAG, "entering text: "+content+" at location: "+x_coord+","+y_coord);
        ArrayList<AccessibilityNodeInfo> nodes = new ArrayList<>();
        getAccessibilityNodeByLocation(x_coord, y_coord, getRootInActiveWindow(), nodes);
        for(AccessibilityNodeInfo node: nodes){
            Log.i(TAG, "node class name: "+node.getClassName());
            if(node != null & node.getClassName().equals("android.widget.EditText")){
                Bundle arguments = new Bundle();
                arguments.putCharSequence(AccessibilityNodeInfo.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE, content);
                node.performAction(AccessibilityNodeInfo.ACTION_SET_TEXT, arguments);
            }
        }

    }

    public void getAccessibilityNodeByLocation(int x, int y, AccessibilityNodeInfo node, ArrayList<AccessibilityNodeInfo> results) {
        if (node == null) return;

        if (node.getChildCount() == 0) {
            Rect buttonRect = new Rect();
            node.getBoundsInScreen(buttonRect);
            if (buttonRect.contains(x, y)) results.add(node);
        } else {
            Rect buttonRect = new Rect();
            node.getBoundsInScreen(buttonRect);
            if (buttonRect.contains(x, y)) results.add(node);
            for (int i = 0; i < node.getChildCount(); i++) {
                getAccessibilityNodeByLocation(x, y, node.getChild(i), results);
            }
        }
    }


    private void appWait(long milli_s_duration){
        try {
            Log.i(TAG, "waiting");
            Thread.sleep(milli_s_duration);
        } catch (Exception e){
            Log.e(TAG, e.toString());
        }
    }

    private void click(float x, float y){
        Log.i(TAG, "clicking: "+x+","+y);
        Path click = new Path();
        click.moveTo(x,y);
        click.lineTo(x, y+5);
        GestureDescription.StrokeDescription stroke = new GestureDescription.StrokeDescription(click, 10, 300);
        GestureDescription.Builder gesture_builder = new GestureDescription.Builder();
        gesture_builder.addStroke(stroke);
        GestureDescription gest_descript = gesture_builder.build();
        dispatchGesture(gest_descript, null, null);
    }

    private void scan(){
        click(scanner.scan_x, scanner.scan_y);
        appWait(scanner.wait_millis);
        click(scanner.share_x,scanner.share_y);
        appWait(scanner.wait_millis);
        click(scanner.drive_x,scanner.drive_y);
        appWait(scanner.wait_millis);
        //label output
        Timestamp ts = new Timestamp(System.currentTimeMillis());
        String label = app_name + "."+ sdf.format(ts);
        enterText(label, (int) scanner.title_x, (int) scanner.title_y);
        click(scanner.save_x,scanner.save_y);
        appWait(scanner.wait_millis);
        click(back_x,back_y);
        appWait(scanner.wait_millis);
        Log.i(TAG, "end scan");
    }
}
