from textwrap import dedent

from masht import md_to_html


def test_a_markdown_file(tmp_path):
    md = tmp_path / "test.md"
    md.write_text(
        dedent(
            """
            # Heading 1

            ## Heading 2

            ### Heading 3

            [bogusoft](https://www.bogusoft.com/)

            List of:

            - stuff
            - fluff
            - snuff

            List using asterisk:

            * stuff
            * fluff
            * fuzz

            ---

            """
        )
    )
    assert md.exists()
    md_to_html.main([str(md)])
    ht = md.with_suffix(".md.AS.html")
    assert ht.exists()


def test_a_markdown_file_with_list_not_preceeded_by_blank_line(tmp_path, capsys):
    md = tmp_path / "test-lists.md"
    md.write_text(
        dedent(
            """
            # Heading 1

            ## Heading 2

            ### Heading 3

            [bogusoft](https://www.bogusoft.com/)

            List of:

            - stuff
            - fluff
            - snuff

            List using asterisk:
            * stuff
            * fluff
            * fuzz

            ---
            """
        )
    )

    assert md.exists()
    md_to_html.main([str(md)])
    ht = md.with_suffix(".md.AS.html")
    assert ht.exists()
    captured = capsys.readouterr()
    assert (
        "WARNING: Lists should be preceeded by a blank line. At line 17."
        in captured.out
    )

    #  Open the test-output file in the default browser.
    # import webbrowser as wb
    # wb.open_new_tab(f"file://{ht}")


def test_file_does_not_exist(tmp_path, capsys):
    non_existent_file = tmp_path / "non_existent.md"
    md_to_html.main([str(non_existent_file)])
    captured = capsys.readouterr()
    assert f"ERROR: '{non_existent_file}' does not exist." in captured.out


def test_not_a_markdown_file(tmp_path, capsys):
    not_md_file = tmp_path / "test.txt"
    not_md_file.write_text("This is not a markdown file.")
    md_to_html.main([str(not_md_file)])
    captured = capsys.readouterr()
    assert f"ERROR: '{not_md_file}' is not a Markdown file." in captured.out


def test_md_to_html_correct_output(tmp_path):
    md_file = tmp_path / "test.md"
    md_file.write_text("# Heading\nThis is a test markdown file.")
    md_to_html.main([str(md_file)])
    out_file = md_file.with_suffix(".md.AS.html")
    assert out_file.exists()
    html_content = out_file.read_text()
    assert "<h1>Heading</h1>" in html_content
    assert "<p>This is a test markdown file.</p>" in html_content


def test_main_no_arguments(capsys):
    md_to_html.main([])
    captured = capsys.readouterr()
    assert "\nUSAGE: masht filename.md [filename2.md ...]\n" in captured.out


def test_main_help(capsys):
    md_to_html.main(["-h"])
    captured = capsys.readouterr()
    assert "\nUSAGE: masht filename.md [filename2.md ...]\n" in captured.out


def test_main_single_argument(tmp_path):
    md_file = tmp_path / "test.md"
    md_file.write_text("# Heading\nThis is a test markdown file.")
    md_to_html.main([str(md_file)])
    out_file = md_file.with_suffix(".md.AS.html")
    assert out_file.exists()


def test_main_multiple_arguments(tmp_path):
    md_file1 = tmp_path / "test1.md"
    md_file1.write_text("# Heading\nThis is a test markdown file.")
    md_file2 = tmp_path / "test2.md"
    md_file2.write_text("# Heading\nThis is another test markdown file.")
    md_to_html.main([str(md_file1), str(md_file2)])
    out_file1 = md_file1.with_suffix(".md.AS.html")
    out_file2 = md_file2.with_suffix(".md.AS.html")
    assert out_file1.exists()
    assert out_file2.exists()


def test_markdown_with_fenced_code_blocks(tmp_path):
    md = tmp_path / "test.md"
    md.write_text(
        dedent(
            """
            # Heading 1
            Here's a muili-line `fenced code block`:
            ```
            def myfunc(rocks=True):
                if rocks:
                    print("Woohoo!")
                else:
                    print("meh")
            # Comment
            ```
            """
        )
    )
    assert md.exists()
    md_to_html.main([str(md)])
    ht = md.with_suffix(".md.AS.html")
    assert ht.exists()
    html_content = ht.read_text()
    #  Multi-line code block should be wrapped in <pre><code>...</code></pre>
    assert "<pre><code>def myfunc(rocks=True):" in html_content
