Напишіть програму обробки папки "Хлам", яка сортує файли у вказаній папці за розширеннями з використанням декількох потоків. Прискорьте обробку великих каталогів з великою кількістю вкладених папок та файлів за рахунок паралельного виконання обходу всіх папок в окремих потоках. Найвитратнішим за часом буде перенесення файлу та отримання списку файлів у папці (ітерація вмісту каталогу). Щоб прискорити перенесення файлів, його можна виконувати в окремому потоці або пулі потоків. Це тим паче зручніше, що результат цієї операції ви в застосунку не обробляєте і можна не збирати жодних результатів. Щоб прискорити обхід вмісту каталогу з кількома рівнями вкладеності, ви можете обробку кожного підкаталогу виконувати в окремому потоці або передавати обробку в пул потоків.