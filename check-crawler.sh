#!/bin/bash
# Quick script to check crawler status

echo "=== Crawler Status Check ==="
echo ""

# Check if process is running
if ps aux | grep -i "crawler.py" | grep -v grep > /dev/null; then
    echo "✅ Crawler is RUNNING"
    ps aux | grep -i "crawler.py" | grep -v grep | awk '{print "   PID:", $2, "| Started:", $9, $10}'
else
    echo "❌ Crawler is NOT running (finished or stopped)"
fi

echo ""

# Count files
PLAYER_COUNT=$(find public/data/players -name '*.json' 2>/dev/null | wc -l | tr -d ' ')
TEAM_COUNT=$(find public/data/teams -name '*.json' 2>/dev/null | wc -l | tr -d ' ')
EXPECTED=5104

echo "📊 Progress:"
echo "   Player files: $PLAYER_COUNT / $EXPECTED"
if [ "$EXPECTED" -gt 0 ]; then
    PROGRESS=$(echo "scale=1; $PLAYER_COUNT * 100 / $EXPECTED" | bc)
    echo "   Progress: ${PROGRESS}%"
fi
echo "   Team files: $TEAM_COUNT"

echo ""

# Check most recent file
if [ -n "$(ls -t public/data/players/*.json 2>/dev/null | head -1)" ]; then
    RECENT=$(ls -t public/data/players/*.json 2>/dev/null | head -1)
    RECENT_TIME=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$RECENT" 2>/dev/null || stat -c "%y" "$RECENT" 2>/dev/null | cut -d' ' -f1,2)
    echo "🕐 Most recent file:"
    echo "   Created: $RECENT_TIME"
fi

echo ""
echo "To check again, run: ./check-crawler.sh"
