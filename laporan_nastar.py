import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
file_path = "data/Laporan Nastar.xlsx"
xls = pd.ExcelFile(file_path)
df_sales = pd.read_excel(xls, sheet_name="Sheet1")
df_costs = pd.read_excel(xls, sheet_name="Sheet2")

# Harga per toples
harga_toples = {"600g": 70000, "550g": 65000, "400g": 50000}
potongan_per_toples = 5000

def save_data():
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df_sales.to_excel(writer, sheet_name="Sheet1", index=False)
        df_costs.to_excel(writer, sheet_name="Sheet2", index=False)
        
def calculate_profit():
    # Hitung total pendapatan
    total_pendapatan = df_sales['Total Harga'].sum()
    
    # Hitung total biaya produksi
    total_biaya = df_costs['Harga'].sum()
    
    # Hitung profit
    profit = total_pendapatan - total_biaya
    
    return total_pendapatan, total_biaya, profit

def main():
    global df_sales, df_costs
    st.set_page_config(page_title="📊 Analisis Penjualan Nastar", layout="wide")
    st.title("🍍 Analisis Penjualan Nastar")
    
        # Tambahkan tombol logout di pojok kanan atas
    col_logout, _ = st.columns([1, 5])
    with col_logout:
        if st.button("🚪 Logout"):
            js = "window.location.href = './';"  # Redirect ke root (main.py)
            st.components.v1.html(f"<script>{js}</script>", height=0)
    # Tab navigasi
    tab1, tab2, tab3 = st.tabs(["📈 Dashboard", "🛒 CRUD Penjualan", "📦 CRUD Biaya Produksi"])

    with tab1:
        st.markdown("### Filter Data")
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            pembayaran_filter = st.radio("Status Pembayaran", ["Semua", "Sudah Bayar", "Belum Bayar"])
        with col_filter2:
            kategori_filter = st.radio("Kategori Pembelian", ["Semua", "Lebaran", "Sekarang"])

        # Filter data
        df_filtered = df_sales.copy()
        if pembayaran_filter != "Semua":
            df_filtered = df_filtered[df_filtered["Sudah Bayar"] == pembayaran_filter]
        if kategori_filter != "Semua":
            df_filtered = df_filtered[df_filtered["Lebaran / Sekarang"] == kategori_filter]

        # Statistik utama
        st.markdown("### 📌 Ringkasan Penjualan")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Pendapatan", f"Rp{df_filtered['Total Harga'].sum():,.0f}")
        with col2:
            st.metric("Rata-rata Harga", f"Rp{df_filtered['Total Harga'].mean():,.0f}")
        with col3:
            st.metric("Total Toples Terjual", df_filtered['Total Toples'].sum())
        with col4:
            st.metric("Total Belum Bayar", f"Rp{df_sales[df_sales['Sudah Bayar'] == 'Belum Bayar']['Total Harga'].sum():,.0f}")

        # Visualisasi
        st.markdown("### 📊 Visualisasi Data")
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("**Total Harga per Pembeli**")
            fig = px.bar(df_filtered, x="Pembeli", y="Total Harga", text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
        
        with col_chart2:
            st.markdown("**Distribusi Status Pembayaran**")
            fig = px.pie(df_sales, names="Sudah Bayar", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
            
        # Hitung profit
        total_pendapatan, total_biaya, profit = calculate_profit()
        
        # Update statistik utama
        st.markdown("### 📌 Ringkasan Penjualan")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Pendapatan", f"Rp{total_pendapatan:,.0f}")
        with col2:
            st.metric("Total Biaya Produksi", f"Rp{total_biaya:,.0f}", delta_color="inverse")
        with col3:
            st.metric("Profit Bersih", f"Rp{profit:,.0f}", 
                    delta=f"{(profit/total_pendapatan*100 if total_pendapatan !=0 else 0):.1f}% Margin")
        with col4:
            st.metric("Total Belum Bayar", f"Rp{df_sales[df_sales['Sudah Bayar'] == 'Belum Bayar']['Total Harga'].sum():,.0f}")

        # Visualisasi profit
        st.markdown("### 📊 Analisis Profit")
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            profit_df = pd.DataFrame({
                'Kategori': ['Pendapatan', 'Biaya', 'Profit'],
                'Nilai': [total_pendapatan, total_biaya, profit]
            })
            fig = px.bar(profit_df, x='Kategori', y='Nilai', text_auto=',.0f',
                       title="Perbandingan Pendapatan vs Biaya vs Profit",
                       color='Kategori',
                       color_discrete_map={
                           'Pendapatan': '#00CC96',
                           'Biaya': '#EF553B',
                           'Profit': '#636EFA'
                       })
            st.plotly_chart(fig, use_container_width=True)
        
        with col_chart2:
            fig = px.pie(values=[total_pendapatan, total_biaya], 
                       names=['Pendapatan', 'Biaya'],
                       title="Komposisi Pendapatan dan Biaya",
                       hole=0.4)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 📜 Data Terfilter")
        st.dataframe(df_filtered, use_container_width=True)

    with tab2:
        st.header("Kelola Data Penjualan")
        
        # Form Tambah Data
        with st.expander("Tambah Data Baru"):
            with st.form("Tambah Data"):
                pembeli = st.text_input("Nama Pembeli*")
                col1, col2, col3 = st.columns(3)
                with col1:
                    toples_600g = st.number_input("Toples 600g", min_value=0)
                with col2:
                    toples_550g = st.number_input("Toples 550g", min_value=0)
                with col3:
                    toples_400g = st.number_input("Toples 400g", min_value=0)
                
                total_harga = (
                    (toples_600g * harga_toples["600g"]) + 
                    (toples_550g * harga_toples["550g"]) + 
                    (toples_400g * harga_toples["400g"])
                )
                
                potongan = st.number_input("Jumlah Potongan", min_value=0)
                total_harga -= potongan * potongan_per_toples
                
                col4, col5 = st.columns(2)
                with col4:
                    status = st.selectbox("Status Pembayaran", ["Sudah Bayar", "Belum Bayar"])
                with col5:
                    kategori = st.selectbox("Kategori", ["Lebaran", "Sekarang"])
                
                if st.form_submit_button("Simpan Data"):
                    if not pembeli:
                        st.error("Nama pembeli wajib diisi!")
                    else:
                        new_data = {
                            "Pembeli": pembeli,
                            "600g": toples_600g,
                            "550g": toples_550g,
                            "400g": toples_400g,
                            "Total Toples": toples_600g + toples_550g + toples_400g,
                            "Potongan 5k/Toples": potongan,
                            "Total Harga": total_harga,
                            "Sudah Bayar": status,
                            "Lebaran / Sekarang": kategori
                        }
                        df_sales.loc[len(df_sales)] = new_data
                        save_data()
                        st.success("Data berhasil disimpan!")

        # Edit & Hapus Data
        with st.expander("Edit/Hapus Data Exist"):
            selected_pembeli = st.selectbox("Pilih Pembeli", df_sales["Pembeli"].unique())
            selected_data = df_sales[df_sales["Pembeli"] == selected_pembeli].iloc[0]

            col6, col7 = st.columns(2)
            with col6:
                st.markdown("### Edit Data")
                with st.form("Edit Data"):
                    new_pembeli = st.text_input("Nama Pembeli", value=selected_data["Pembeli"])
                    new_600g = st.number_input("Toples 600g", value=selected_data["600g"], key="edit_600g")
                    new_550g = st.number_input("Toples 550g", value=selected_data["550g"], key="edit_550g")
                    new_400g = st.number_input("Toples 400g", value=selected_data["400g"], key="edit_400g")
                    new_potongan = st.number_input("Potongan", value=selected_data["Potongan 5k/Toples"])
                    new_status = st.selectbox("Status", ["Sudah Bayar", "Belum Bayar"], 
                                           index=0 if selected_data["Sudah Bayar"] == "Sudah Bayar" else 1)
                    new_kategori = st.selectbox("Kategori", ["Lebaran", "Sekarang"],
                                              index=0 if selected_data["Lebaran / Sekarang"] == "Lebaran" else 1)
                    
                    if st.form_submit_button("Update Data"):
                        df_sales.loc[df_sales["Pembeli"] == selected_pembeli, [
                            "Pembeli", "600g", "550g", "400g", "Potongan 5k/Toples",
                            "Sudah Bayar", "Lebaran / Sekarang"
                        ]] = [new_pembeli, new_600g, new_550g, new_400g, new_potongan, new_status, new_kategori]
                        save_data()
                        st.success("Data berhasil diupdate!")
            
            with col7:
                st.markdown("### Hapus Data")
                if st.button(f"Hapus Data untuk {selected_pembeli}"):
                    df_sales = df_sales[df_sales["Pembeli"] != selected_pembeli]
                    save_data()
                    st.success("Data berhasil dihapus!")
                    st.rerun()

    with tab3:
        st.header("Kelola Biaya Produksi")
        
        # CRUD Biaya Produksi
        with st.expander("Tambah Data Baru"):
            with st.form("Tambah Biaya"):
                col8, col9, col10 = st.columns(3)
                with col8:
                    nama = st.text_input("Nama Barang*")
                with col9:
                    qty = st.text_input("Quantity*")
                with col10:
                    harga = st.number_input("Harga*", min_value=0)
                
                if st.form_submit_button("Simpan"):
                    if not nama or not qty:
                        st.error("Field bertanda * wajib diisi!")
                    else:
                        new_cost = pd.DataFrame([{
                            "Nama Barang": nama,
                            "Berapa": qty,
                            "Harga": harga
                        }])
                        global df_costs
                        df_costs = pd.concat([df_costs, new_cost], ignore_index=True)
                        save_data()
                        st.success("Data berhasil disimpan!")

        # Edit & Hapus
        with st.expander("Edit/Hapus Data Exist"):
            selected_cost = st.selectbox("Pilih Barang", df_costs["Nama Barang"].unique())
            cost_data = df_costs[df_costs["Nama Barang"] == selected_cost].iloc[0]

            col11, col12 = st.columns(2)
            with col11:
                st.markdown("### Edit Data")
                with st.form("Edit Biaya"):
                    edit_nama = st.text_input("Nama Barang", value=cost_data["Nama Barang"])
                    edit_qty = st.text_input("Quantity", value=cost_data["Berapa"])
                    edit_harga = st.number_input("Harga", value=cost_data["Harga"])
                    
                    if st.form_submit_button("Update"):
                        df_costs.loc[df_costs["Nama Barang"] == selected_cost, [
                            "Nama Barang", "Berapa", "Harga"
                        ]] = [edit_nama, edit_qty, edit_harga]
                        save_data()
                        st.success("Data berhasil diupdate!")
            
            with col12:
                st.markdown("### Hapus Data")
                if st.button(f"Hapus {selected_cost}"):
                    df_costs = df_costs[df_costs["Nama Barang"] != selected_cost]
                    save_data()
                    st.success("Data berhasil dihapus!")
                    st.rerun()

        st.dataframe(df_costs, use_container_width=True)

if __name__ == "__main__":
    main()