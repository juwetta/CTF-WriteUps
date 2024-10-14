import re
import ast
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

'''
Modified Version [cleaner code]
However, this script cannot be tested because the connection to the challenge web is lost.
date: 8/9/2024
'''

# Define the function to check if all points are connected
def are_points_connected(point_pairs):
    graph_dict = {}
    degree = {}

    # Build the graph and calculate degrees of all points
    for pair in point_pairs:
        p1, p2 = tuple(pair[0]), tuple(pair[1])
        if p1 not in graph_dict:
            graph_dict[p1] = []
        if p2 not in graph_dict:
            graph_dict[p2] = []
        graph_dict[p1].append(p2)
        graph_dict[p2].append(p1)
        
        degree[p1] = degree.get(p1, 0) + 1
        degree[p2] = degree.get(p2, 0) + 1

    # Check the degree of vertices, count how many have an odd degree
    odd_degree_count = sum(1 for d in degree.values() if d % 2 != 0)

    # Eulerian Path exists if there are exactly 0 or 2 vertices with an odd degree
    if odd_degree_count != 0 and odd_degree_count != 2:
        return False

    # Use BFS to check if all points are connected (ignoring isolated points)
    def bfs(start):
        visited = set()
        queue = [start]
        visited.add(start)
        while queue:
            node = queue.pop(0)
            for neighbor in graph_dict[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return visited

    # Start BFS from any point
    start_point = next(iter(graph_dict))
    visited_points = bfs(start_point)

    # Check if all points in the graph are connected
    return len(visited_points) == len(graph_dict)




def main():
    
    # Set up the web driver (make sure to have ChromeDriver installed and in PATH)
    driver = webdriver.Chrome()

    # Navigate to the website
    driver.get("http://single-line.warzone-challenges.com:9050")

    # Wait for the page to load and press the submit button
    wait = WebDriverWait(driver, 10)

    '''cllick button, begin challenge'''
    try:
        submit_button = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="submit"]')))
        submit_button.click()
        print("Submit button clicked.")
    except Exception as e:
        print(f"Error clicking submit button: {e}")


    # Wait for the challenges page to load
    time.sleep(3)  

    for i in range(302):
        try:
            
            if i == 300:
                time.sleep(20) #so we can read the flag 

            body_text = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body'))).text
            
            # Use regular expressions to extract the points between the "[[[" and "]]]" markers
            points_match = re.search(r'\[\[\[.*?\]\]\]', body_text)
            
            if points_match:
                points_text = points_match.group(0)
                
                # Convert the extracted string into a Python list
                try:
                    points = ast.literal_eval(points_text)
                except Exception as e:
                    print(f"Error parsing points: {e}")
                    continue

                # Check if the points are connected
                answer = "Yes" if are_points_connected(points) else "No"
                
                # Find the answer input field and enter the answer
                try:
                    answer_input = wait.until(EC.presence_of_element_located((By.NAME, 'oneline_drawable')))
                    answer_input.clear()  # Clear the field before entering new input
                    answer_input.send_keys(answer)
                    print(answer)
                    # Submit the answer by clicking the submit button
                    submit_button = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="submit"]')))
                    submit_button.click()
                    
                except Exception as e:
                    time.sleep(1)
                    print(f"Error submitting answer: {e}")
                    continue
            else:
                '''
                debugging purpose, we need the questions when the function return wrong answer
                '''
                print(f"No points found in challenge {i+1}")
                print("wrong", answer)
                print("points: ",points_text)
                break

        except Exception as e:
            print(f"Error during challenge {i+1}: {e}")
            continue

    # Close the driver after completing all challenges
    driver.quit()

main()
