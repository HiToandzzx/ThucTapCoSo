import networkx as nx
import matplotlib.pyplot as plt
import os
from datetime import datetime

def create_graph_from_input():
    while True:
        choice = input("\nChọn một trong hai lựa chọn sau đây:\n1. Nhập dữ liệu từ bàn phím\n2. Nhập dữ liệu từ file txt\nChọn (1 hoặc 2): ")
        
        G = nx.DiGraph()
        pos = None
        
        if choice == '1':
            print("\nNhập cạnh theo định dạng (đỉnh nguồn_đỉnh đích_trọng số)\nEx: 0 1 5:")
            num_edges = int(input("Nhập số cạnh của đồ thị: "))
            for _ in range(num_edges): 
                edge = input().split() 
                source, target, weight = map(int, edge)
                G.add_edge(source, target, weight=weight) 
            pos = nx.circular_layout(G)
            break  # Thoát khỏi vòng lặp nếu dữ liệu nhập là hợp lệ
            
        elif choice == '2':
            current_directory = os.path.dirname(os.path.abspath(__file__)) 
            file_path = os.path.join(current_directory, "input.txt")
            if os.path.exists(file_path): 
                try:
                    with open(file_path, 'r') as file: 
                        lines = file.readlines()
                        for line in lines:
                            edge = list(map(int, line.strip().split()))
                            source, target, weight = edge  
                            G.add_edge(source, target, weight=weight)
                    pos = nx.circular_layout(G)
                    break  # Thoát khỏi vòng lặp nếu dữ liệu nhập là hợp lệ
                except FileNotFoundError:
                    print("Không tìm thấy tệp tin.")
                    return None
            else:
                print("Đường dẫn không chính xác.")
                return None
        else:
            print("\nLựa chọn không hợp lệ. Vui lòng chọn lại.")
    
    return G, pos

# THUẬT TOÁN DFS
def depth_first_search(G, start_node, end_node):
    # Khởi tạo 1 danh sách rỗng để lưu trữ tất cả các đường đi.
    all_paths = [] 

    def dfs_util(u, d, visited, path):
        # Đánh dấu đỉnh u đã được duyệt.
        visited[u] = True 
        # Thêm đỉnh u vào đường đi hiện tại.
        path.append(u) 

        # Nếu đỉnh xuất phát = đỉnh kết thúc.
        if u == d:
            all_paths.append(list(path)) # Lưu lại đường đi đã tìm thấy.
        else:
            # Lặp qua các đỉnh kề của u trong đồ thị G.
            for i in G.neighbors(u): 
                if not visited[i]: 
                    dfs_util(i, d, visited, path)

        # Trở về trạng thái trước đó.
        path.pop() 
        # Đánh dấu đỉnh u chưa được duyệt để có thể duyệt nó qua các đường đi khác.
        visited[u] = False 

    # Tạo một từ điển visited có các khóa là các đỉnh trong đồ thị G.
    visited = {node: False for node in G.nodes()} 
    dfs_util(start_node, end_node, visited, [])

    # In ra trong console các đường đi đã tìm được
    if not all_paths:
        return []

    # Trả về danh sách all_paths
    return all_paths

# TẠO MA TRẬN KỀ
def create_adjacency_matrix(G):
    # Chuyển đồ thị G thành một ma trận kề dưới dạng một mảng NumPy.
    adjacency_matrix = nx.convert_matrix.to_numpy_array(G) 
    return adjacency_matrix

# LƯU CÁC ĐƯỜNG ĐI MIN/MAX
def save_paths(matrix, all_paths, value, file_name):
    current_time = datetime.now().strftime('%d''/''%m''_''%H'':''%M')
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, file_name)
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            if not all_paths:
                file.write(f"\nKhông tìm thấy đường đi từ đỉnh {start_node} đến đỉnh {end_node}!!!\n")
            else:
                if value:
                    file.write(f"\n\n{current_time}\nMa trận kề:\n {matrix}\n")
                    shortest_path = min(all_paths, key=len)
                    file.write(f"\nĐường đi ngắn nhất từ đỉnh {start_node} đến đỉnh {end_node}: {' -> '.join(map(str, shortest_path))}\n")
                else:
                    file.write(f"\n\n{current_time}\nMa trận kề:\n {matrix}\n")
                    longest_path = max(all_paths, key=len)
                    file.write(f"\nĐường đi dài nhất từ đỉnh {start_node} đến đỉnh {end_node}: {' -> '.join(map(str, longest_path))}\n")
    except FileNotFoundError:
        print("Không tìm thấy tệp tin.")
        return None
    
# LƯU CÁC ĐƯỜNG ĐI CÓ TRỌNG SỐ MIN/MAX
def save_weights(matrix, all_paths, value, file_name):
    current_time = datetime.now().strftime('%d''/''%m''_''%H'':''%M')
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, file_name)
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            if not all_paths:  
                file.write(f"\nKhông tìm thấy đường đi từ đỉnh {start_node} đến đỉnh {end_node}!!!\n")
            else: 
                if value:
                    file.write(f"\n\n{current_time}\nMa trận kề:\n {matrix}\n")
                    min_path = min(all_paths_with_weights, key=lambda x: sum(x.values()))
                    file.write(f"\nĐường đi có trọng số nhỏ nhất: {min_path}, trọng số {min_weight}\n")
                else:
                    file.write(f"\n\n{current_time}\nMa trận kề:\n {matrix}\n")
                    max_path = max(all_paths_with_weights, key=lambda x: sum(x.values()))
                    file.write(f"\nĐường đi có trọng số lớn nhất: {max_path}, trọng số {max_weight}\n")
    except FileNotFoundError:
        print("Không tìm thấy tệp tin.")
        return None
    
# HÀM THOÁT CHƯƠNG TRÌNH
def exit_program():
    while True:
        print("\n       BẠN CÓ MUỐN TIẾP TỤC CHƯƠNG TRÌNH?")
        print("==============================================")
        print("1. Tiếp tục")
        print("2. Thoát")
        choice = input("Nhập lựa chọn: ")

        if choice == '1':
            return True  # Trả về True nếu người dùng muốn tiếp tục
        elif choice == '2':
            print("\nĐã thoát chương trình.\n")
            return False  # Trả về False nếu người dùng muốn thoát
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

def check():
    for source, target, data in G.edges(data=True):
        edge_labels = {(source, target): data.get('weight')}  
        
        if G.has_edge(target, source):
            nx.draw(G, pos, with_labels=True, node_size=900, font_size=15, node_color='skyblue', edgelist=[(source, target)], arrows=True, connectionstyle="arc3,rad=0.3")
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, bbox=dict(alpha=0), label_pos=0.8, verticalalignment='center') 
        else:
            nx.draw(G, pos, with_labels=True, node_size=900, font_size=15, node_color='skyblue', edgelist=[(source, target)], arrows=True)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, verticalalignment='bottom', bbox=dict(alpha=0))     


# TẠO ĐỒ THỊ TỪ INPUT
graph_data = create_graph_from_input()

if graph_data:
    while True:
        G, pos = graph_data

        # HIỂN THỊ MA TRẬN KỀ Ở CONSOLE
        adjacency_matrix = create_adjacency_matrix(G)
        print("\nMa trận kề của đồ thị:")
        print(adjacency_matrix)

        print("\n           TÌM ĐƯỜNG ĐI TRONG ĐỒ THỊ CÓ HƯỚNG")
        print("=======================================================")
        print("1. Tìm đường đi ngắn nhất.")
        print("2. Tìm đường đi dài nhất.")
        print("3. Tìm đường đi có tổng trọng số nhỏ nhất.")
        print("4. Tìm đường đi có tổng trọng số lớn nhất.")
        option = input("Nhập lựa chọn: ")

        # TÌM ĐƯỜNG ĐI NGẮN NHẤT VÀ DÀI NHẤT
        if option == '1':
            start_node = int(input("\nNhập đỉnh bắt đầu: "))
            end_node = int(input("Nhập đỉnh đích: "))
            all_paths = depth_first_search(G, start_node, end_node)

            if all_paths:
                shortest_path = min(all_paths, key=len)  

                edges_to_plot = [(shortest_path[j], shortest_path[j + 1]) for j in range(len(shortest_path) - 1)]

                print(f"\nĐường đi ngắn nhất từ đỉnh {start_node} đến đỉnh {end_node}: {' -> '.join(map(str, shortest_path))}")
                
                plt.figure(figsize=(10, 5)) 
                plt.subplot(1, 2, 1)
                plt.title("Đồ thị gốc")
                check()

                plt.tight_layout()

                plt.subplot(1, 2, 2)
                plt.title("Đường đi ngắn nhất")  
                check() 

                for source, target in edges_to_plot:  
                    plt.pause(1.5)
                    if G.has_edge(target, source):
                        nx.draw_networkx_edges(G, pos, edgelist=[(source, target)], edge_color='red', width=2.0, connectionstyle="arc3,rad=0.3")
                    else:
                        nx.draw_networkx_edges(G, pos, edgelist=[(source, target)], edge_color='red', width=2.0)
                
                plt.pause(1)
                plt.tight_layout()
                plt.show()

                # Gọi hàm lưu các đường đi vào file
                save_paths(adjacency_matrix, all_paths, True, "output_paths.txt")  

                # Gọi hàm để xử lý lựa chọn tiếp tục hoặc thoát
                if not exit_program():  
                    break

            else:
                print(f"\nKhông có đường đi từ đỉnh {start_node} đến đỉnh {end_node}!!!\n")

        elif option == '2':
            start_node = int(input("\nNhập đỉnh bắt đầu: "))
            end_node = int(input("Nhập đỉnh đích: "))
            all_paths = depth_first_search(G, start_node, end_node)

            if all_paths:
                longest_path = max(all_paths, key=len)  

                print(f"\nĐường đi dài nhất từ đỉnh {start_node} đến đỉnh {end_node}: {' -> '.join(map(str, longest_path))}")

                plt.figure(figsize=(10, 5)) 
                plt.subplot(1, 2, 1)
                plt.title("Đồ thị gốc")
                check() 

                plt.tight_layout()

                plt.subplot(1, 2, 2)
                plt.title("Đường đi dài nhất")  
                check()

                # Danh sách các cặp đỉnh liền kề trên đường đi ngắn nhất 
                edges_to_plot = [(longest_path[j], longest_path[j + 1]) for j in range(len(longest_path) - 1)]

                for source, target in edges_to_plot:  
                    plt.pause(1.5)
                    if G.has_edge(target, source):
                        nx.draw_networkx_edges(G, pos, edgelist=[(source, target)], edge_color='red', width=2.0, connectionstyle="arc3,rad=0.3")
                    else:
                        nx.draw_networkx_edges(G, pos, edgelist=[(source, target)], edge_color='red', width=2.0)

                plt.pause(1)
                plt.tight_layout()
                plt.show()

                # Gọi hàm lưu các đường đi vào file
                save_paths(adjacency_matrix, all_paths, False, "output_paths.txt")  

                # Gọi hàm để xử lý lựa chọn tiếp tục hoặc thoát
                if not exit_program():  
                    break

            else:
                print(f"\nKhông có đường đi từ đỉnh {start_node} đến đỉnh {end_node}!!!\n")

        # TÌM ĐƯỜNG ĐI CÓ TRỌNG SỐ NHỎ NHẤT VÀ LỚN NHẤT
        elif option == '3':
            start_node = int(input("\nNhập đỉnh bắt đầu: "))
            end_node = int(input("Nhập đỉnh đích: "))
            all_paths = depth_first_search(G, start_node, end_node)

            if all_paths:
                # Tạo ra một danh sách chứa các từ điển. 
                # Mỗi từ điển trong danh sách này ánh xạ từ cặp đỉnh liên tiếp trong mỗi đường đi (path) đến trọng số của cạnh nối chúng trong đồ thị.
                all_paths_with_weights = [
                    {(path[i], path[i + 1]): G[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1)} 
                    for path in all_paths
                ]

                # Sử dụng tham số key để chỉ định tiêu chí để tìm đối tượng (trọng số).
                min_path = min(all_paths_with_weights, key=lambda x: sum(x.values()))

                # Tính tổng trọng số của đường đi có tổng trọng số nhỏ nhất.
                # Hàm values() trả về danh sách các giá trị (trọng số của các cạnh) trong từ điển.
                min_weight = sum(min_path.values()) 

                print(f"\nĐường đi có tổng trọng số nhỏ nhất từ đỉnh {start_node} đến {end_node}: {min_weight}")
                print(min_path)

                plt.figure(figsize=(10, 5))
                plt.subplot(1, 2, 1)
                plt.title("Đồ thị gốc")
                check()

                plt.tight_layout()

                plt.subplot(1, 2, 2)
                plt.title("Đường đi có tổng trọng số nhỏ nhất")
                check()

                # Tạo 1 danh sách các cặp đỉnh tương ứng với cạnh trong đường đi có trọng số nhỏ nhất (min_path).
                edges_to_plot = [(edge[0], edge[1]) for edge in min_path.keys()]

                for source, target in edges_to_plot:  
                    plt.pause(1.5)
                    if G.has_edge(target, source):
                        nx.draw_networkx_edges(G, pos, edgelist=[(source, target)], edge_color='red', width=2.0, connectionstyle="arc3,rad=0.3")
                    else:
                        nx.draw_networkx_edges(G, pos, edgelist=[(source, target)], edge_color='red', width=2.0)

                plt.pause(1)
                plt.tight_layout()
                plt.show()

                # Gọi hàm lưu các đường đi vào file
                save_weights(adjacency_matrix, all_paths, 1, "output_weights.txt")

                # Gọi hàm để xử lý lựa chọn tiếp tục hoặc thoát
                if not exit_program():  
                    break

            else:
                print(f"\nKhông có đường đi từ đỉnh {start_node} đến đỉnh {end_node}!!!\n")

        elif option == '4':
            start_node = int(input("\nNhập đỉnh bắt đầu: "))
            end_node = int(input("Nhập đỉnh đích: "))
            all_paths = depth_first_search(G, start_node, end_node)

            if all_paths:
                # Tạo ra một danh sách chứa các từ điển. 
                # Mỗi từ điển trong danh sách này ánh xạ từ cặp đỉnh liên tiếp trong mỗi đường đi (path) đến trọng số của cạnh nối chúng trong đồ thị.
                all_paths_with_weights = [
                    {(path[i], path[i + 1]): G[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1)} 
                    for path in all_paths
                ]

                # Sử dụng tham số key để chỉ định tiêu chí để tìm đối tượng (trọng số).
                max_path = max(all_paths_with_weights, key=lambda x: sum(x.values()))

                # Tính tổng trọng số của đường đi có tổng trọng số nhỏ nhất.
                # Hàm values() trả về danh sách các giá trị (trọng số của các cạnh) trong từ điển.
                max_weight = sum(max_path.values()) 

                print(f"\nĐường đi có tổng trọng số  lớn nhất từ đỉnh {start_node} đến {end_node}: {max_weight}")
                print(max_path)

                plt.figure(figsize=(10, 5))
                plt.subplot(1, 2, 1)
                plt.title("Đồ thị gốc")
                check()

                plt.tight_layout()

                plt.subplot(1, 2, 2)
                plt.title("Đường đi có tổng trọng số lớn nhất")
                check()

                # Tạo 1 danh sách các cặp đỉnh tương ứng với cạnh trong đường đi có trọng số nhỏ nhất (min_path).
                edges_to_plot = [(edge[0], edge[1]) for edge in max_path.keys()]

                for source, target in edges_to_plot:  
                    plt.pause(1.5)
                    if G.has_edge(target, source):
                        nx.draw_networkx_edges(G, pos, edgelist=[(source, target)], edge_color='red', width=2.0, connectionstyle="arc3,rad=0.3")
                    else:
                        nx.draw_networkx_edges(G, pos, edgelist=[(source, target)], edge_color='red', width=2.0)

                plt.pause(1)
                plt.tight_layout()
                plt.show()

                # Gọi hàm lưu các đường đi vào file
                save_weights(adjacency_matrix, all_paths, 0, "output_weights.txt")

                # Gọi hàm để xử lý lựa chọn tiếp tục hoặc thoát
                if not exit_program():  
                    break

            else:
                print(f"\nKhông có đường đi từ đỉnh {start_node} đến đỉnh {end_node}!!!\n")

        else:
            print("\nLựa chọn không hợp lệ.")





        



