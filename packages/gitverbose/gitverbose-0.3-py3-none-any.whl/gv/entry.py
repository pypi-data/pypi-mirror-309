import argparse
from git_clone import git_clone
import urllib.request

# funções

def clone(repo, external):
    if not external:
        print('Received file')
        if repo.startswith("https://github.com") and repo.endswith(".git"):
            print('Cloning repository..')
            git_clone(repo)
        else:
            print('Please insert a valid github repository url!')
    elif external:
        print('Received file')
        if repo.startswith("https://") and repo.endswith(".git"):
            print('Cloning repository..')
            git_clone(repo)
            print('Cloned project with success!')
        else:
            print('Please insert a valid external repository url!')
        
        
        
def fclone(file, output_file):
    if file:
        print('Please insert a valid url.')
        print(f'Received file. {file}')
        print('Writing file..')
        try:
            urllib.request.urlretrieve(file)
        except Exception as e:
            print(e)
    elif file and output_file:
        print('Please insert a valid url.')
        print(f'Received file. {output_file}')
        print('Writing file..')
        try:
            urllib.request.urlretrieve(file, output_file)
        except Exception as e:
            print(e)





# ponto de entrada ( para a ferramenta funcionar)
def gv_entry_point():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    
    # argumentos
    parser_clone = subparsers.add_parser('clone', help='Clone a github repository')
    parser_clone.add_argument('repo', help='The repository that will be cloned')
    parser_clone.add_argument('-ex', '--external', help='External github repository that will be cloned')
    
    
    parser_fclone = subparsers.add_parser('fclone', help='Clone a internet file')
    parser_fclone.add_argument('file', help='The file url')
    parser_fclone.add_argument('-o', '--output-file', help='Output file (example: -o coolfile.png)')
    
    
    # verificações de commando 
    args = parser.parse_args()
    
    if args.command == 'clone':
        clone(args.repo, args.external)
    elif args.command == 'xclone':
        fclone(args.file, args.output_file)
    else:
        parser.print_help()