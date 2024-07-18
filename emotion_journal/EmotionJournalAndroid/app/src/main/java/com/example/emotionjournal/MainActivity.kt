package com.example.emotionjournal

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import okhttp3.*
import java.io.IOException

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        NotificationUtils.scheduleNotification(this)

        // Example call to send an emotion to the server
        sendEmotionToServer("happy", "Feeling great!", "Morning routine", "Woke up refreshed", 8)
    }

    private fun sendEmotionToServer(
        mainCategory: String,
        subCategory: String,
        trigger: String,
        description: String,
        rating: Int
    ) {
        val client = OkHttpClient()
        val url = "http://your_flask_server/api/emotions"

        val json = """
            {
                "main_category": "$mainCategory",
                "sub_category": "$subCategory",
                "trigger": "$trigger",
                "description": "$description",
                "rating": $rating
            }
        """.trimIndent()

        val body = RequestBody.create(MediaType.get("application/json; charset=utf-8"), json)
        val request = Request.Builder()
            .url(url)
            .post(body)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                runOnUiThread {
                    Toast.makeText(this@MainActivity, "Failed to send emotion", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onResponse(call: Call, response: Response) {
                if (response.isSuccessful) {
                    runOnUiThread {
                        Toast.makeText(this@MainActivity, "Emotion sent successfully", Toast.LENGTH_SHORT).show()
                    }
                } else {
                    runOnUiThread {
                        Toast.makeText(this@MainActivity, "Failed to send emotion", Toast.LENGTH_SHORT).show()
                    }
                }
            }
        })
    }
}
