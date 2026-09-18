# run this from the project root
# all the other configs are in the project root
uv run nuitka `
    --mode=onefile `
    --include-data-files="src/life_analytics/sql/*.sql=life_analytics/sql/" `
    --output-dir=dist/onefile/ `
    --assume-yes-for-downloads `
    src/life_analytics/main.py

# remove all useless build junk
Remove-Item "dist/onefile/main.build" -Recurse -Force
Remove-Item "dist/onefile/main.onefile-build" -Recurse -Force

# now we creating the standalone version
uv run nuitka `
    --mode=standalone `
    --include-data-files="src/life_analytics/sql/*.sql=life_analytics/sql/" `
    --output-dir=dist/standalone/ `
    --assume-yes-for-downloads `
    src/life_analytics/main.py

# remove all useless build junk
Remove-Item "dist/standalone/main.build" -Recurse -Force

# add the readme from assets
Copy-Item `
    "assets/README.txt" `
    "dist/standalone/README.txt"

Move-Item "dist/onefile/life.exe" "dist/life-windows-x86_64.exe"
Rename-Item "dist/standalone/main.dist" "life"

Compress-Archive `
    -Path "dist/standalone/*" `
    -DestinationPath "dist/life-windows-x86_64-standalone.zip" `
    -Force

Remove-Item "dist/onefile/" -Recurse -Force
Remove-Item "dist/standalone/" -Recurse -Force
