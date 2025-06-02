<?php
function aiResponse($message) {
    $message = strtolower(trim($message));
    
    if (strpos($message, 'samir') !== false) {
        return "Samir Puri is a developer from Nepal (Chitwan, Bharatpur), currently living in Sydney. He created this AI!";
    } elseif (strpos($message, 'weather') !== false) {
        return "I'm a basic AI and cannot fetch live weather yet. Try adding an API!";
    } elseif (strpos($message, 'hi') !== false || strpos($message, 'hello') !== false) {
        return "Hello! How can I help you today?";
    } else {
        return "Sorry, I don't understand that yet. Try asking about Samir!";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Samir's AI Agent</title>
</head>
<body>
    <h2>Chat with Samir's AI</h2>
    <form method="post">
        <input type="text" name="message" placeholder="Say something..." required>
        <input type="submit" value="Ask">
    </form>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $userMessage = $_POST["message"];
        echo "<p><strong>You:</strong> " . htmlspecialchars($userMessage) . "</p>";
        echo "<p><strong>Bot:</strong> " . aiResponse($userMessage) . "</p>";
    }
    ?>
</body>
</html>
