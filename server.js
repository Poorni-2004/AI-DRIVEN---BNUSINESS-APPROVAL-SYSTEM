const express = require("express");
const nodemailer = require("nodemailer");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
app.use(cors());  // Allow frontend requests
app.use(bodyParser.json());

let storedOTP = {};  // Temporary storage for OTPs

// Configure Nodemailer Transporter
const transporter = nodemailer.createTransport({
    service: "gmail",
    auth: {
        user: "poornimam927@gmail.com", // Replace with your Gmail
        pass: "pqexbyzaqqmwqfjk"        // Replace with your Gmail App Password
    },
});

// Endpoint to send OTP
app.post("/send-otp", (req, res) => {
    const { email } = req.body;

    if (!email) {
        return res.status(400).json({ error: "Recipient email is missing!" });
    }

    const otp = Math.floor(100000 + Math.random() * 900000); // 6-digit OTP
    storedOTP[email] = otp;

    const mailOptions = {
        from: "poornimam927@gmail.com",
        to: email,
        subject: "Your OTP Code",
        text: `Your OTP is: ${otp}. It is valid for 5 minutes.`,
    };

    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            console.error("Error sending email:", error);
            return res.status(500).json({ error: "Failed to send OTP" });
        }
        console.log("Email sent:", info.response);
        res.json({ message: "OTP sent successfully" }); // Do not send OTP to frontend
    });
});

// Endpoint to verify OTP
app.post("/verify-otp", (req, res) => {
    const { email, otp } = req.body;

    if (storedOTP[email] && storedOTP[email] == otp) {
        delete storedOTP[email];  // OTP verified, remove it
        return res.json({ success: true, message: "OTP verified successfully!" });
    }

    return res.status(400).json({ success: false, message: "Invalid OTP" });
});

app.listen(3000, () => {
    console.log("Server running on port 3000");
});
