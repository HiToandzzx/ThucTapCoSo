import networkx as nx
import matplotlib.pyplot as plt
import os
from datetime import datetime

def create_graph_from_input():
    choice = input("\nChọn một trong hai lựa chọn sau đây:\n1. Nhập dữ liệu từ bàn phím\n2. Nhập dữ liệu từ file txt\nChọn (1 hoặc 2): ")
    
    G = nx.DiGraph()
    pos = None
    
    # LỰA CHỌN 1: NHẬP DỮ LIỆU TỪ BÀN PHÍM
    if choice == '1':
        print("\nNhập cạnh theo định dạng (đỉnh nguồn_đỉnh đích_trọng số)\nEx: 0 1 5:")
        num_edges = int(input("Nhập số cạnh của đồ thị: "))
        for _ in range(num_edges): # Lặp số lần bằng số cạnh.
            edge = input().split() # Chuyển đổi chuỗi nhập thành một danh sách các thành phần, tách nhau bởi khoảng trắng.
            source, target, weight= map(int, edge) # Sử dụng map để chuyển đổi các phần tử trong danh sách edge từ chuỗi thành số nguyên.
            G.add_edge(source, target, weight=weight) # Thêm cạnh mới vào đồ thị.
        
        # VẼ ĐỒ THỊ
        pos = nx.circular_layout(G) # Sử dụng layout dạng hình tròn.
        
    # LỰA CHỌN 2: LẤY DỮ LIỆU TỪ FILE TXT
    elif choice == '2':
        current_directory = os.path.dirname(os.path.abspath(__file__)) # Lấy đường dẫn tuyệt đối đến thư mục chứa tệp đang thực thi chương trình.
        file_path = os.path.join(current_directory, "input.txt") # Tạo đường dẫn tới file "input.txt" trong cùng thư mục với file đang thực thi.
        if os.path.exists(file_path): # Nếu file txt có tồn tại thì:
            try:
                with open(file_path, 'r') as file: # Mở file và đọc từng dòng.
                    lines = file.readlines()
                    for line in lines:
                        edge = list(map(int, line.strip().split()))
                        source, target, weight = edge  # Lấy thông tin trọng số từ dòng
                        G.add_edge(source, target, weight=weight)
                        
                pos = nx.circular_layout(G)
            except FileNotFoundError:
                print("Không tìm thấy tệp tin.")
                return None
        else:
            print("Đường dẫn không chính xác.")
            return None
        
    else:
        print("Lựa chọn không hợp lệ.")
        return None
    
    return G, pos

# THUẬT TOÁN DFS
def depth_first_search(G, start_node, end_node):
    all_paths = [] # Khởi tạo 1 danh sách rỗng để lưu trữ tất cả các đường đi.

    # u: đỉnh hiện tại đang xét,
    # d: đỉnh kết thúc,
    # visited: đánh dấu các đỉnh đã được duyệt,
    # path: đường đi hiện tại từ start_node đến u.
    def dfs_util(u, d, visited, path):
        visited[u] = True # Đánh dấu đỉnh u đã được duyệt.
        path.append(u) # Thêm đỉnh u vào đường đi hiện tại.

        # Nếu đỉnh xuất phát = đỉnh kết thúc.
        if u == d:
            all_paths.append(list(path)) # Lưu lại đường đi đã tìm thấy.
        else:
            for i in G.neighbors(u): # Lặp qua các đỉnh kề của u trong đồ thị G.
                if not visited[i]: # Nếu đỉnh kề i chưa được duyệt, gọi đệ quy để tiếp tục tìm kiếm đường đi từ u đến d.
                    dfs_util(i, d, visited, path)

        path.pop() # Trở về trạng thái trước đó của đường đi bằng cách loại bỏ đỉnh u ra khỏi path.
        visited[u] = False # Đánh dấu đỉnh u chưa được duyệt để có thể duyệt nó qua các đường đi khác.

    visited = {node: False for node in G.nodes()} # Tạo một từ điển visited có các khóa là các đỉnh trong đồ thị G và giá trị ban đầu của tất cả các đỉnh là False, đánh dấu rằng chưa có đỉnh nào được duyệt.
    dfs_util(start_node, end_node, visited, [])

    # In ra trong console các đường đi đã tìm được
    if not all_paths:
        return []

    # Trả về danh sách all_paths
    return all_paths

# TẠO MA TRẬN KỀ
def create_adjacency_matrix(G):
    adjacency_matrix = nx.convert_matrix.to_numpy_array(G) # Chuyển đồ thị G thành một ma trận kề dưới dạng một mảng NumPy.
    return adjacency_matrix

# LƯU MA TRẬN KỀ VÀO FILE
def save_matrix_to_file(matrix, file_name):
    current_time = datetime.now().strftime('%d''/''%m''_''%H'':''%M')
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, file_name)
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"\n\n{current_time}\nMa trận kề:\n {matrix}\n")
    except FileNotFoundError:
        print("Không tìm thấy tệp tin.")
        return None

# LƯU CÁC ĐƯỜNG ĐI VÀO FILE TXT
def save_paths_to_file(all_paths, file_name):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, file_name)

    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            if not all_paths:  # If no paths are found
                file.write(f"\nKhông tìm thấy đường đi từ đỉnh {start_node} đến đỉnh {end_node}!!!\n")
            else:  # Paths are found
                shortest_path = min(all_paths, key=len)  # Find the shortest path
                longest_path = max(all_paths, key=len)  # Find the longest path

                if (shortest_path != longest_path):
                    file.write(f"\nCác đường đi đã tìm được từ đỉnh {start_node} đến đỉnh {end_node}:\n")
                    file.write(f"\nĐường đi ngắn nhất: {' -> '.join(map(str, shortest_path))}\n")
                    file.write(f"Đường đi dài nhất: {' -> '.join(map(str, longest_path))}\n")
                else:
                    file.write(f"\nChỉ có 1 đường đi đã tìm được từ đỉnh {start_node} đến đỉnh {end_node}:\n")
                    file.write(f"\nĐường đi: {' -> '.join(map(str, shortest_path))}\n")
    except FileNotFoundError:
        print("Không tìm thấy tệp tin.")
        return None
    
# LƯU CÁC ĐƯỜNG ĐI CÓ TRỌNG SỐ MIN / MAX
def save_dijkastra(all_paths, file_name):
    current_time = datetime.now().strftime('%d''/''%m''_''%H'':''%M')
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, file_name)

    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            if not all_paths:  # If no paths are found
                file.write(f"\nKhông tìm thấy đường đi từ đỉnh {start_node} đến đỉnh {end_node}!!!\n")
            else:  # Paths are found
                min_path = min(all_paths_with_weights, key=lambda x: sum(x.values()))
                max_path = max(all_paths_with_weights, key=lambda x: sum(x.values()))

                if (min_path != max_path):
                    file.write(f"\nCác đường đi đã tìm được từ đỉnh {start_node} đến đỉnh {end_node}:\n")
                    file.write(f"\nĐường đi có trọng số nhỏ nhất: {min_path}, trọng số {min_weight}\n")
                    file.write(f"Đường đi có trọng số lớn nhất: {max_path}, trọng số {max_weight}")
                else:
                    file.write(f"\nĐường đi có trọng số nhỏ nhất và lớn nhất: {min_path}, trọng số {min_weight}\n")


    except FileNotFoundError:
        print("Không tìm thấy tệp tin.")
        return None

# TẠO ĐỒ THỊ TỪ INPUT
graph_data = create_graph_from_input()

while True:

    if graph_data:
        G, pos = graph_data

        # HIỂN THỊ MA TRẬN KỀ Ở CONSOLE
        adjacency_matrix = create_adjacency_matrix(G)
        print("\nMa trận kề của đồ thị:")
        print(adjacency_matrix)

        print("\n           TÌM ĐƯỜNG ĐI TRONG ĐỒ THỊ CÓ HƯỚNG")
        print("=======================================================")
        print("1. Tìm đường đi ngắn nhất và dài nhất.")
        print("2. Tìm đường đi có tổng trọng số nhỏ nhất và lớn nhất.")
        option = input("Nhập lựa chọn: ")

        # TÌM ĐƯỜNG ĐI NGẮN NHẤT VÀ DÀI NHẤT
        if option == '1':
            start_node = int(input("\nNhập đỉnh bắt đầu: "))
            end_node = int(input("Nhập đỉnh đích: "))
            all_paths = depth_first_search(G, start_node, end_node)

            if all_paths:
                shortest_path = min(all_paths, key=len)  
                longest_path = max(all_paths, key=len)   

                if len(shortest_path) == len(longest_path):
                    print(f"\nChỉ có 1 đường đi từ đỉnh {start_node} đến đỉnh {end_node}")
                    print(f"Đường đi: {' -> '.join(map(str, shortest_path))}")

                    plt.figure(figsize=(10, 5)) 
                    plt.subplot(1, 2, 1)
                    plt.title("Đồ thị gốc")
                    # Từ điển lưu trữ thông tin về trọng số của các cạnh trong đồ thị
                    # (i, j): int(weight): Cặp khóa-giá trị trong từ điển, với i và j là các đỉnh và weight là trọng số.
                    # Duyệt qua tất cả các cạnh trong đồ thị G và lấy thông tin về trọng số của chúng
                    edge_labels = {(i, j): int(weight) for i, j, weight in G.edges(data='weight')} 
                    nx.draw(G, pos, with_labels=True, node_size=900, node_color='skyblue', font_weight='bold', arrows=True)
                    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels) # Hiển thị trọng số

                    plt.subplot(1, 2, 2)
                    plt.title("Đường đi")  
                    edge_labels = {(i, j): int(weight) for i, j, weight in G.edges(data='weight')}  
                    nx.draw(G, pos, with_labels=True, node_size=900, node_color='skyblue', font_weight='bold', arrows=True)
                    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels) # Hiển thị trọng số
                    # Danh sách các cặp đỉnh liền kề trên đường đi ngắn nhất 
                    edges_to_plot = [(shortest_path[j], shortest_path[j + 1]) for j in range(len(shortest_path) - 1)]

                    for edge in edges_to_plot:
                        plt.tight_layout()
                        plt.pause(1.5)
                        nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='red', width=3.0)
                        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

                    plt.pause(1)

                    plt.tight_layout()
                    plt.show()

                else:
                    print(f"\nCác đường đi từ đỉnh {start_node} đến đỉnh {end_node}")
                    print(f"Đường đi ngắn nhất: {' -> '.join(map(str, shortest_path))}")
                    print(f"Đường đi dài nhất: {' -> '.join(map(str, longest_path))}")

                    plt.figure(figsize=(15, 5))  
                    plt.subplot(1, 3, 1)  
                    plt.title("Đồ thị gốc")
                    edge_labels = {(i, j): int(weight) for i, j, weight in G.edges(data='weight')}  
                    nx.draw(G, pos, with_labels=True, node_size=900, node_color='skyblue', font_weight='bold', arrows=True)
                    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)  

                    # Danh sách chứa hai đường đi
                    paths_to_plot = [shortest_path, longest_path]

                    # Duyệt qua danh sách paths_to_plot
                    for i, path in enumerate(paths_to_plot):
                        plt.tight_layout()
                        # subplot 1 hàng, 3 cột với chỉ số của subplot được tính từ i + 2
                        plt.subplot(1, 3, i + 2)
                        plt.title(f"{'Đường đi ngắn nhất' if i == 0 else 'Đường đi dài nhất'}")
                        nx.draw(G, pos, with_labels=True, node_size=900, node_color='skyblue', font_weight='bold', arrows=True)
                        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)  

                        # Tạo danh sách các cặp đỉnh liên tiếp trong đường đi path.
                        edges = [(path[j], path[j + 1]) for j in range(len(path) - 1)]

                        for edge in edges:
                            plt.pause(1.5)
                            nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='red' if i == 0 else 'blue', width=3.0)
                            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)  

                        plt.pause(1)

                    plt.tight_layout()
                    plt.show()    

            else:
                print(f"\nKhông có đường đi từ đỉnh {start_node} đến đỉnh {end_node}!!!\n")

            # Gọi hàm để hiển thị ma trận kề của đồ thị và lưu vào file 
            save_matrix_to_file(adjacency_matrix, "output_DFS.txt") 
            
            # Gọi hàm lưu các đường đi vào file
            save_paths_to_file(all_paths, "output_DFS.txt")  

        # TÌM ĐƯỜNG ĐI CÓ TRỌNG SỐ NHỎ NHẤT VÀ LỚN NHẤT
        elif option == '2':
            start_node = int(input("\nNhập đỉnh bắt đầu: "))
            end_node = int(input("Nhập đỉnh đích: "))
            all_paths = depth_first_search(G, start_node, end_node)

            if all_paths:
                # Tạo ra một danh sách chứa các từ điển. 
                # Mỗi từ điển trong danh sách này ánh xạ từ cặp đỉnh liên tiếp trong mỗi đường đi (path) đến trọng số của cạnh nối chúng trong đồ thị.
                
                # for i in range(len(path) - 1): Vòng lặp duyệt qua các chỉ số từ 0 đến len(path) - 2.
                # (path[i], path[i + 1]): Tạo ra một cặp đỉnh liên tiếp trong đường đi path.
                # G[path[i]][path[i + 1]]['weight']: Lấy trọng số của cạnh nối giữa hai đỉnh liên tiếp trong đồ thị G.
                
                all_paths_with_weights = [
                    {(path[i], path[i + 1]): G[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1)} 
                    for path in all_paths
                ]

                # Sử dụng tham số key để chỉ định tiêu chí để tìm đối tượng (trọng số).
                min_path = min(all_paths_with_weights, key=lambda x: sum(x.values()))
                max_path = max(all_paths_with_weights, key=lambda x: sum(x.values()))

                # Tính tổng trọng số của đường đi có tổng trọng số nhỏ nhất.
                # Hàm values() trả về danh sách các giá trị (trọng số của các cạnh) trong từ điển.
                min_weight = sum(min_path.values()) 
                max_weight = sum(max_path.values()) 

                if min_weight != max_weight:
                    print(f"\nĐường đi có tổng trọng số nhỏ nhất là: {min_weight}")
                    print(min_path)
                    print(f"\nĐường đi có tổng trọng số lớn nhất là: {max_weight}")
                    print(max_path)

                    plt.figure(figsize=(15, 5))
                    plt.subplot(1, 3, 1)
                    plt.title("Đồ thị gốc")
                    edge_labels = {(i, j): int(weight) for i, j, weight in G.edges(data='weight')}
                    nx.draw(G, pos, with_labels=True, node_size=900, node_color='skyblue', font_weight='bold', arrows=True)
                    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

                    # Tạo 1 danh sách
                    paths_to_plot = [min_path, max_path]

                    for i, path in enumerate(paths_to_plot):
                        plt.tight_layout()
                        plt.subplot(1, 3, i + 2)
                        plt.title(f"{'Đường đi trọng số min' if i == 0 else 'Đường đi trọng số max'}")
                        nx.draw(G, pos, with_labels=True, node_size=900, node_color='skyblue', font_weight='bold', arrows=True)
                        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

                        # Tạo danh sách các cặp đỉnh từ các khóa trong từ điển path.
                        edges = [(u, v) for (u, v) in path.keys()]

                        for edge in edges:
                            plt.pause(1.5)
                            nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='red' if i == 0 else 'blue', width=3.0)
                            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

                        plt.pause(1)

                    plt.tight_layout()
                    plt.show()

                else:
                    print(f"\nĐường đi có tổng trọng số nhỏ nhất và lớn nhất là {min_weight} từ đỉnh {start_node} đến {end_node}:")
                    print(min_path)

                    plt.figure(figsize=(10, 5))
                    plt.subplot(1, 2, 1)
                    plt.title("Đồ thị gốc")
                    edge_labels = {(i, j): int(weight) for i, j, weight in G.edges(data='weight')}
                    nx.draw(G, pos, with_labels=True, node_size=900, node_color='skyblue', font_weight='bold', arrows=True)
                    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels) # Hiển thị trọng số

                    plt.subplot(1, 2, 2)
                    plt.title("Đường đi có tổng trọng số min, max")
                    edge_labels = {(i, j): int(weight) for i, j, weight in G.edges(data='weight')}
                    nx.draw(G, pos, with_labels=True, node_size=900, node_color='skyblue', font_weight='bold', arrows=True)
                    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)  # Hiển thị trọng số
                    # Tạo 1 danh sách các cặp đỉnh tương ứng với cạnh trong đường đi có trọng số nhỏ nhất (min_path).
                    # Duyệt qua các khóa trong từ điển min_path.
                    edges_to_plot = [(edge[0], edge[1]) for edge in min_path.keys()]

                    for edge in edges_to_plot:
                        plt.tight_layout()
                        plt.pause(1.5)
                        nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='red', width=3.0)
                        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

                    plt.pause(1)

                    plt.tight_layout()
                    plt.show()

            else:
                print(f"\nKhông có đường đi từ đỉnh {start_node} đến đỉnh {end_node}!!!\n")

            # Gọi hàm để hiển thị ma trận kề của đồ thị và lưu vào file 
            save_matrix_to_file(adjacency_matrix, "output_Dijkstra.txt") 

            # Gọi hàm lưu các đường đi vào file
            save_dijkastra(all_paths, "output_Dijkstra.txt")  

        else:
            print("\nLựa chọn không hợp lệ.")
    
        print("\nBẠN CÓ MUỐN TIẾP TỤC CHƯƠNG TRÌNH?")
        print("1. Tiếp tục")
        print("2. Thoát")
        choice = input("Nhập lựa chọn: ")

        if choice == '1':
            continue  # Quay lại để người dùng nhập lựa chọn tìm đường đi mới
        elif choice == '2':
            print("\nĐã thoát chương trình.\n")
            break  
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")



            



