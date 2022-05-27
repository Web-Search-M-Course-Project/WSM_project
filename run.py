import argparse
parser = argparse.ArgumentParser(description='WSM Group Project')
parser.add_argument('--generate-meta-data', action='store_true', default=False,
                        help='generate meta data')
parser.add_argument('--generate-inverted-index', action='store_true', default=False,
                        help='generate inverted index')
args = parser.parse_args()
import utlis
utlis.picklize()

# generate meta_data
print("generate_meta_data:", args.generate_meta_data)
if args.generate_meta_data:
    import parse_data
    print("generate_meta_data: ok")
print()

# generate inverted index
print("generate_inverted_index:", args.generate_inverted_index)
if args.generate_inverted_index:
    import nltk
    import index.inverted_index
    from index.inverted_index import construct_inverted_index
    construct_inverted_index(fussy_method='none')
    construct_inverted_index(fussy_method='stem')
    construct_inverted_index(fussy_method='lemmatize')
    print("generate_inverted_index: ok")
print()

utlis.picklize()
