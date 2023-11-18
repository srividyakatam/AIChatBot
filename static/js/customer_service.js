$(document).ready(function() {
    window.onload = function() {
        fetch('/clear-chat')
        .then(response => response.text())
        .then(data => console.log(data));
        };
    
      document.getElementById('submitQuery').addEventListener('click', sendMessage);
    
      document.getElementById('userQuery').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
          sendMessage();
        }
      });
    
      function sendMessage() {
        let userMessage = document.getElementById('userQuery').value;
        let serviceType = document.getElementById('serviceType').value; 
        if (!userMessage.trim()) return; // Prevents sending empty messages

        var selectedContext = $('#context-selector').val();
        var selectedPersonality = $('#personality-selector').val();
        var selectedResponseLanguage = $('#language-selector').val();
    
        let chatbox = document.getElementById('chatbox');
        chatbox.innerHTML += `<div class="user-message">${userMessage}</div>`;
        
    
        fetch('/customer_service_chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({'message': userMessage,
          'service_type': serviceType,
          'context': selectedContext,
          'personality': selectedPersonality,
          'language': selectedResponseLanguage })
        })
        .then(response => response.json())
        .then(data => {
          chatbox.innerHTML += `<div class="bot-message">${data.message}</div>`;
          updatePromptLog(data.prompt); // Update the prompt log
          chatbox.scrollTop = chatbox.scrollHeight; // Scroll to latest message
        });
    
        document.getElementById('userQuery').value = ''; // Clear input field
      }
      
      document.getElementById('exportButton').addEventListener('click', exportChat);
      function exportChat() {
        let serviceType = document.getElementById('serviceType').value; // Get the service type
        window.location.href = `/customer_service_export-chat/${serviceType}`;
    }
    
    function updatePromptLog(promptText) {
      let promptLog = document.getElementById('promptLog');
      let newPrompt = document.createElement('div');
      newPrompt.classList.add('prompt-entry');

      // Adding timestamp
      let timestamp = new Date().toLocaleTimeString();
      newPrompt.innerHTML = `<span class="timestamp">${timestamp}:</span> ${promptText}`;

      promptLog.appendChild(newPrompt);
      promptLog.scrollTop = promptLog.scrollHeight; // Scroll to the latest prompt

      // Limit the number of prompts in the log
      let maxPrompts = 10; // Adjust as needed
      while (promptLog.children.length > maxPrompts) {
        promptLog.removeChild(promptLog.firstChild);
      }

      // Copy prompt functionality
      newPrompt.onclick = function() {
        copyToClipboard(promptText, this);
      };

      function copyToClipboard(text, promptElement) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
    
        // Show tooltip
        showTooltip(promptElement, 'Copied!');
      }
    }

    function showTooltip(element, message) {
        const tooltip = document.createElement('span');
        tooltip.className = 'tooltip';
        tooltip.textContent = message;
        document.body.appendChild(tooltip);
    
        // Position the tooltip
        const rect = element.getBoundingClientRect();
        tooltip.style.left = `${rect.left + window.scrollX}px`;
        tooltip.style.top = `${rect.bottom + window.scrollY + 5}px`;
    
        // Remove the tooltip after 2 seconds
        setTimeout(() => {
            document.body.removeChild(tooltip);
        }, 2000);
    }

    document.getElementById('exportPromptButton').addEventListener('click', function() {
      let serviceType = document.getElementById('serviceType').value;
      window.location.href = `/customer_service_export-prompts/${serviceType}`;  });
  

  
});
